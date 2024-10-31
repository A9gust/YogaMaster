from flask import Flask, request, jsonify
from flask_cors import CORS
import io
from PIL import Image
import numpy as np
import pandas as pd
from ultralytics import YOLO
from comparison import calculate_angle, calculate_thresholds_for_each_image, calculate_symmetry
from openai import OpenAI

zhipu_client = OpenAI(api_key="4e236fbfb2e80cfa3e1b642ab90d8ad1.fgLD1XCw9F5IqQ5g", base_url="https://open.bigmodel.cn/api/paas/v4/")

def zhipu_model(message):
    messages = [{"role": "user", "content": message}]
    completion = zhipu_client.chat.completions.create(
        model="glm-4-0520",
        messages=messages,
        top_p=0.7,
        temperature=0.9
    )
    return completion.choices[0].message.content

# 初始化 Flask 应用
app = Flask(__name__)
CORS(app)  # 允许跨域请求

# 初始化 YOLO 模型
model = YOLO("yolo11n-pose.pt")

# 读取 CSV 文件中的预定义阈值
angle_thresholds = pd.read_csv("thresholds_angle_output2.csv")
max_thresholds = pd.read_csv("pose_max_threshold_values.csv")

# 定义对称性要求
symmetry_requirements = {
    'symmetry_required': ['goddess_pose', 'chair_pose', 'downward-facing_dog_pose'],
    'symmetry_partial_required': ['tree_pose'],
    'symmetry_not_required': ['warrior_1_pose', 'warrior_2_pose', 'warrior_3_pose', 
                              'side_plank_pose', 'low_lunge_pose', 'lord_of_the_dance_pose']
}

# 生成反馈
def generate_feedback(angle_comparison, symmetry_comparison):
    feedback = []
    
    # 处理角度反馈
    for angle_name, comparison in angle_comparison.items():
        if comparison == 0:
            feedback.append(f"您的 {angle_name} 超出了最大允许角度，请稍微调整。")
        elif comparison == -1:
            feedback.append(f"您的 {angle_name} 小于最小允许角度，请稍微调整。")
        else:
            feedback.append(f"您的 {angle_name} 看起来不错，保持这个姿势。")
    
    # 处理对称性反馈
    for key, value in symmetry_comparison.items():
        if value is None:
            continue  # 对于不需要对称的部分忽略
        elif value == False:
            feedback.append(f"您的 {key} 需要更对称一些。")
        else:
            feedback.append(f"您的 {key} 对称性很好。")
    
    return " ".join(feedback)


# 处理上传的图片并进行姿势分析
def analyze_pose(image, label):
    # 使用 YOLO 模型预测关键点
    results = model(image)
    data = []
    
    for r in results:
        keypoints = r.keypoints.xyn.cpu().numpy()[0]
        keypoints = keypoints.reshape((1, keypoints.shape[0] * keypoints.shape[1]))[0].tolist()
        data.append(keypoints)

    # 创建 DataFrame 保存关键点数据
    total_features = len(data[0])
    df = pd.DataFrame(data=data, columns=[f"x{i}" for i in range(total_features)])
    
    # 计算关节角度
    angles = []
    for i in range(len(df)):
        left_shoulder = df[['x10', 'x11']].to_numpy()[i]
        left_elbow = df[['x14', 'x15']].to_numpy()[i]
        left_wrist = df[['x18', 'x19']].to_numpy()[i]
        right_shoulder = df[['x12', 'x13']].to_numpy()[i]
        right_elbow = df[['x16', 'x17']].to_numpy()[i]
        right_wrist = df[['x20', 'x21']].to_numpy()[i]
        left_hip = df[['x22', 'x23']].to_numpy()[i]
        left_knee = df[['x26', 'x27']].to_numpy()[i]
        left_ankle = df[['x30', 'x31']].to_numpy()[i]
        right_hip = df[['x24', 'x25']].to_numpy()[i]
        right_knee = df[['x28', 'x29']].to_numpy()[i]
        right_ankle = df[['x32', 'x33']].to_numpy()[i]

        # 计算各关节的角度
        left_elbow_angle = calculate_angle(left_shoulder, left_elbow, left_wrist)
        right_elbow_angle = calculate_angle(right_shoulder, right_elbow, right_wrist)
        left_knee_angle = calculate_angle(left_hip, left_knee, left_ankle)
        right_knee_angle = calculate_angle(right_hip, right_knee, right_ankle)
        hip_angle = calculate_angle(left_knee, left_hip, left_shoulder)

        angles.append({
            'left_elbow': left_elbow_angle,
            'right_elbow': right_elbow_angle,
            'left_knee': left_knee_angle,
            'right_knee': right_knee_angle,
            'hip_angle': hip_angle
        })

    # 转换为 DataFrame
    angles_df = pd.DataFrame(angles)

    # 初始化关键点索引的字典
    keypoint_indices = {
        'left_shoulder': ['x10', 'x11'],
        'left_elbow': ['x14', 'x15'],
        'left_wrist': ['x18', 'x19'],
        'right_shoulder': ['x12', 'x13'],
        'right_elbow': ['x16', 'x17'],
        'right_wrist': ['x20', 'x21'],
        'left_hip': ['x22', 'x23'],
        'left_knee': ['x26', 'x27'],
        'left_ankle': ['x30', 'x31'],
        'right_hip': ['x24', 'x25'],
        'right_knee': ['x28', 'x29'],
        'right_ankle': ['x32', 'x33']
    }

    # 根据 label 从阈值表中获取最大和最小阈值
    threshold_row = max_thresholds[max_thresholds['label'] == label].iloc[0]
    angle_row = angle_thresholds[angle_thresholds['label'] == label].iloc[0]
    
    # 计算角度并与阈值比较
    comparison_results = {
        'left_elbow': compare_with_thresholds(angles_df['left_elbow'].values[0], angle_row, 'left_elbow'),
        'right_elbow': compare_with_thresholds(angles_df['right_elbow'].values[0], angle_row, 'right_elbow'),
        'left_knee': compare_with_thresholds(angles_df['left_knee'].values[0], angle_row, 'left_knee'),
        'right_knee': compare_with_thresholds(angles_df['right_knee'].values[0], angle_row, 'right_knee')
    }

    # 计算对称性
    result = {'label': label}
    if label in symmetry_requirements['symmetry_required']:
        # 使用预定义阈值进行对称性计算
        symmetry_result = calculate_symmetry_for_pose(df, 0, keypoint_indices, threshold_row)
        result.update({
            'shoulder_symmetry_correct': symmetry_result['shoulder_symmetry'],
            'hip_symmetry_correct': symmetry_result['hip_symmetry'],
            'knee_symmetry_correct': symmetry_result['knee_symmetry'],
            'ankle_symmetry_correct': symmetry_result['ankle_symmetry']
        })
    elif label in symmetry_requirements['symmetry_partial_required']:
        # 只检测部分部位对称性
        symmetry_result = calculate_symmetry_for_pose(df, 0, keypoint_indices, threshold_row)
        result.update({
            'shoulder_symmetry_correct': symmetry_result['shoulder_symmetry'],
            'hip_symmetry_correct': symmetry_result['hip_symmetry'],
            'knee_symmetry_correct': None,  # 不需要膝盖对称
            'ankle_symmetry_correct': None  # 不需要脚踝对称
        })
    else:
        # 不需要对称性计算
        result.update({
            'shoulder_symmetry_correct': None,
            'hip_symmetry_correct': None,
            'knee_symmetry_correct': None,
            'ankle_symmetry_correct': None
        })
    # 生成反馈
    feedback = generate_feedback(comparison_results, result)
    message = f"我会给你提供一段瑜伽建议，请帮我进行润色且提供一些建议，在保证信息完整化的情况下尽量简化输出，尤其要去掉反复重复的部分。只输出英语结果就行：{feedback}"
    zhipu_result = zhipu_model(message)

    # 返回角度、对称性和反馈结果
    return {
        'angles': comparison_results,
        'symmetry': result,
        'feedback': zhipu_result
    }


# 比较关节角度与阈值
def compare_with_thresholds(angle, angle_row, angle_name):
    if angle > angle_row[f'max_{angle_name}']:
        return 0  # 超过最大阈值
    elif angle < angle_row[f'min_{angle_name}']:
        return -1  # 低于最小阈值
    else:
        return 1  # 在阈值范围内


# 计算对称性
def calculate_symmetry_for_pose(df, i, keypoint_indices, thresholds):
    shoulder_threshold = thresholds['shoulder_threshold']
    hip_threshold = thresholds['hip_threshold']
    knee_threshold = thresholds['knee_threshold']
    ankle_threshold = thresholds['ankle_threshold']

    return {
        'shoulder_symmetry': calculate_symmetry(df.loc[i, keypoint_indices['left_shoulder']].values, 
                                                df.loc[i, keypoint_indices['right_shoulder']].values, 
                                                shoulder_threshold),
        'hip_symmetry': calculate_symmetry(df.loc[i, keypoint_indices['left_hip']].values, 
                                           df.loc[i, keypoint_indices['right_hip']].values, 
                                           hip_threshold),
        'knee_symmetry': calculate_symmetry(df.loc[i, keypoint_indices['left_knee']].values, 
                                            df.loc[i, keypoint_indices['right_knee']].values, 
                                            knee_threshold),
        'ankle_symmetry': calculate_symmetry(df.loc[i, keypoint_indices['left_ankle']].values, 
                                             df.loc[i, keypoint_indices['right_ankle']].values, 
                                             ankle_threshold)
    }




# # Flask 路由用于处理前端上传的图片
# @app.route('/api/upload', methods=['POST'])
# def upload_photo():
#     if 'photo' not in request.files:
#         return jsonify({'error': 'No file part'}), 400

#     photo = request.files['photo']
    
#     if photo.filename == '':
#         return jsonify({'error': 'No selected file'}), 400
    
#     try:
#         # 读取图片并将其转换为 numpy 数组
#         image = Image.open(photo)
#         np_image = np.array(image)

#         # 假设前端会传递姿势 label，如果没有传递，则默认值为 'downward-facing_dog_pose'
#         label = request.form.get('pose_label', 'downward-facing_dog_pose')  # 默认为下犬式

#         # 调用姿势分析函数
#         analysis_result = analyze_pose(np_image, label)
#         feedback = analysis_result['feedback']

#         # 返回反馈给前端
#         return jsonify({'reply': feedback})

#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

@app.route('/api/upload', methods=['POST'])
def upload_photo():
    try:
        if 'photo' not in request.files:
            print("No file part in request")
            return jsonify({'error': 'No file part'}), 400

        photo = request.files['photo']

        if photo.filename == '':
            print("No selected file")
            return jsonify({'error': 'No selected file'}), 400

        try:
            # 读取图片并将其转换为 RGB 格式（如果需要）
            image = Image.open(photo)

            # 检查图片的模式，如果是 RGBA 或者其他格式，将其转换为 RGB
            if image.mode != 'RGB':
                print(f"Converting image from {image.mode} to RGB")
                image = image.convert('RGB')

            # 将图片转换为 numpy 数组
            np_image = np.array(image)
            print(f"Photo '{photo.filename}' successfully processed.")
        except Exception as e:
            print(f"Error opening the image: {str(e)}")
            return jsonify({'error': 'Failed to open image file'}), 500

        label = request.form.get('pose_label', 'downward-facing_dog_pose')
        print(f"Pose label: {label}")

        try:
            analysis_result = analyze_pose(np_image, label)
            feedback = analysis_result['feedback']
            print("Pose analysis completed successfully.")
        except Exception as e:
            print(f"Error analyzing pose: {str(e)}")
            return jsonify({'error': 'Pose analysis failed'}), 500

        return jsonify({'reply': feedback})

    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500


# @app.route('/api/upload', methods=['POST'])
# def upload_photo():
#     try:
#         # 1. 检查是否有文件在请求中
#         if 'photo' not in request.files:
#             print("No file part in request")  # 记录日志
#             return jsonify({'error': 'No file part'}), 400

#         photo = request.files['photo']
        
#         # 2. 检查文件名是否为空
#         if photo.filename == '':
#             print("No selected file")  # 记录日志
#             return jsonify({'error': 'No selected file'}), 400

#         # 3. 打印接收到的文件名
#         print(f"Received file: {photo.filename}")

#         # 这里可以添加图片处理的逻辑，假设是一个函数 process_photo()
#         # result = process_photo(photo)

#         # 4. 模拟成功处理
#         return jsonify({'reply': '照片处理成功！'})  # 返回成功信息

#     except Exception as e:
#         # 5. 捕获并打印错误详细信息
#         print(f"Error occurred: {str(e)}")  # 将错误打印到终端
#         return jsonify({'error': 'Internal Server Error: ' + str(e)}), 500  # 返回详细的错误信息给前端

if __name__ == '__main__':
    app.run(debug=True, port=8000)

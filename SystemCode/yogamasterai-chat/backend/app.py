from flask import Flask, request, jsonify
from flask_cors import CORS
import io
from PIL import Image
import numpy as np
import pandas as pd
from ultralytics import YOLO
from comparison import calculate_angle, calculate_thresholds_for_each_image, calculate_symmetry
from openai import OpenAI
from flask import url_for
from yoga_database import recommend_yoga_pose
from flask_sqlalchemy import SQLAlchemy 

zhipu_client = OpenAI(api_key="816b16cf194841026ddc86cd6d91729c.Mod39gZggYxfgV2s", base_url="https://open.bigmodel.cn/api/paas/v4/")

def zhipu_model(message):
    messages = [{"role": "user", "content": message}]
    completion = zhipu_client.chat.completions.create(
        model="glm-4-0520",
        messages=messages,
        top_p=0.7,
        temperature=0.9
    )
    return completion.choices[0].message.content

# Init flask
app = Flask(__name__)
CORS(app)  

# Intialize database
app.secret_key = 'secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/yoga'  # For MySQL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), nullable=False)
    password = db.Column(db.Integer, nullable=True)
    goldmember = db.Column(db.String(80), nullable=True)

    def __repr__(self):
        return f'<User {self.name}>'


with app.app_context():
    db.create_all()
# Init YOLO
model = YOLO("yolo11n-pose.pt")

# Read threshold
angle_thresholds = pd.read_csv("thresholds_angle_output2.csv")
max_thresholds = pd.read_csv("pose_max_threshold_values.csv")

# Define symmetry
symmetry_requirements = {
    'symmetry_required': ['goddess_pose', 'chair_pose', 'downward-facing_dog_pose'],
    'symmetry_partial_required': ['tree_pose'],
    'symmetry_not_required': ['warrior_1_pose', 'warrior_2_pose', 'warrior_3_pose', 
                              'side_plank_pose', 'low_lunge_pose', 'lord_of_the_dance_pose']
}

# Generate feedback
def generate_feedback(angle_comparison, symmetry_comparison):
    feedback = []
    
    # Process angle
    for angle_name, comparison in angle_comparison.items():
        if comparison == 0:
            feedback.append(f"您的 {angle_name} 超出了最大允许角度，请稍微调整。")
        elif comparison == -1:
            feedback.append(f"您的 {angle_name} 小于最小允许角度，请稍微调整。")
        else:
            feedback.append(f"您的 {angle_name} 看起来不错，保持这个姿势。")
    
    # Process symeetry
    for key, value in symmetry_comparison.items():
        if value is None:
            continue  # Igonre 
        elif value == False:
            feedback.append(f"您的 {key} 需要更对称一些。")
        else:
            feedback.append(f"您的 {key} 对称性很好。")
    
    return " ".join(feedback)


# Process uploaded photo
def analyze_pose(image, label):
    # Key-point detection
    results = model(image)
    data = []
    
    for r in results:
        keypoints = r.keypoints.xyn.cpu().numpy()[0]
        keypoints = keypoints.reshape((1, keypoints.shape[0] * keypoints.shape[1]))[0].tolist()
        data.append(keypoints)

    # Create dataframe
    total_features = len(data[0])
    df = pd.DataFrame(data=data, columns=[f"x{i}" for i in range(total_features)])
    
    # Compute angles
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

    angles_df = pd.DataFrame(angles)

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

    # Max and min of threshold
    threshold_row = max_thresholds[max_thresholds['label'] == label].iloc[0]
    angle_row = angle_thresholds[angle_thresholds['label'] == label].iloc[0]
    
    # Compare to threshold
    comparison_results = {
        'left_elbow': compare_with_thresholds(angles_df['left_elbow'].values[0], angle_row, 'left_elbow'),
        'right_elbow': compare_with_thresholds(angles_df['right_elbow'].values[0], angle_row, 'right_elbow'),
        'left_knee': compare_with_thresholds(angles_df['left_knee'].values[0], angle_row, 'left_knee'),
        'right_knee': compare_with_thresholds(angles_df['right_knee'].values[0], angle_row, 'right_knee')
    }

    # Compute symmetry
    result = {'label': label}
    if label in symmetry_requirements['symmetry_required']:
        symmetry_result = calculate_symmetry_for_pose(df, 0, keypoint_indices, threshold_row)
        result.update({
            'shoulder_symmetry_correct': symmetry_result['shoulder_symmetry'],
            'hip_symmetry_correct': symmetry_result['hip_symmetry'],
            'knee_symmetry_correct': symmetry_result['knee_symmetry'],
            'ankle_symmetry_correct': symmetry_result['ankle_symmetry']
        })
    elif label in symmetry_requirements['symmetry_partial_required']:
        # Detect part of the body
        symmetry_result = calculate_symmetry_for_pose(df, 0, keypoint_indices, threshold_row)
        result.update({
            'shoulder_symmetry_correct': symmetry_result['shoulder_symmetry'],
            'hip_symmetry_correct': symmetry_result['hip_symmetry'],
            'knee_symmetry_correct': None, 
            'ankle_symmetry_correct': None 
        })
    else:
        result.update({
            'shoulder_symmetry_correct': None,
            'hip_symmetry_correct': None,
            'knee_symmetry_correct': None,
            'ankle_symmetry_correct': None
        })
    # Generate feedback
    feedback = generate_feedback(comparison_results, result)
    message = f"我会给你提供一段瑜伽建议，请帮我进行润色且提供一些建议，在保证信息完整化的情况下尽量简化输出，尤其要去掉反复重复的部分。并使输出自然并以英文结果输出：{feedback}"
    zhipu_result = zhipu_model(message)

    # Return result
    return {
        'angles': comparison_results,
        'symmetry': result,
        'feedback': zhipu_result
    }


def compare_with_thresholds(angle, angle_row, angle_name):
    if angle > angle_row[f'max_{angle_name}']:
        return 0  # Max
    elif angle < angle_row[f'min_{angle_name}']:
        return -1  # MIN
    else:
        return 1  # IN

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
# @app.route('/api/upload', methods=['POST'])
# def upload_photo():
#     if 'photo' not in request.files:
#         return jsonify({'error': 'No file part'}), 400

#     photo = request.files['photo']
    
#     if photo.filename == '':
#         return jsonify({'error': 'No selected file'}), 400
    
#     try:
#         image = Image.open(photo)
#         np_image = np.array(image)

#         label = request.form.get('pose_label', 'downward-facing_dog_pose')  

#         analysis_result = analyze_pose(np_image, label)
#         feedback = analysis_result['feedback']

#         return jsonify({'reply': feedback})

#     except Exception as e:
#         return jsonify({'error': str(e)}), 500


users = [{"username":'admin',"password":123}]


@app.route('/api/login', methods=['GET', 'POST'])
def login():
    username = request.json["username"]
    password = request.json["password"]
    if (username =='admin' and password == '123')  or (username =='Li Qiuxian' and password == '123'):
        return "success"
    return "username or password wrong"


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
            # Convert to rgb
            image = Image.open(photo)

            if image.mode != 'RGB':
                print(f"Converting image from {image.mode} to RGB")
                image = image.convert('RGB')

            # Convert to numpy
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


@app.route('/api/chat', methods=['POST'])
def chat_with_user():
    try:
        # POST user message
        user_input = request.json.get('message')
        if not user_input:
            return jsonify({'error': 'No message provided'}), 400

        # Process greet
        if any(keyword in user_input.lower() for keyword in ["who are you", "hello", "hi"]):
            return jsonify({
                'reply': "Hello! I'm Yoga Master AI, your virtual yoga assistant. Feel free to ask me any questions about yoga."
            })

        # generate feedback
        try:
            recommended_pose = recommend_yoga_pose(user_input)
        except Exception as e:
            print(f"Error in recommend_yoga_pose: {str(e)}")
            recommended_pose = None   
        if recommended_pose and recommended_pose['name'] != 'Downward-facing Dog Pose':
            # Recommend pose
            image_url = url_for('static', filename=recommended_pose["image_path"].lstrip('/'))
            recommended_pose_data = {
                'name': recommended_pose['name'],
                'image_path': image_url,  # 构建的图片路径
                'description': recommended_pose['description'], 
                'difficulty': recommended_pose['difficulty'],
                'target': recommended_pose['target'],
                'body_parts': recommended_pose['body_parts']
            }
            print(image_url)
            # Recommedn pose
            return jsonify({
                'reply': f"I recommend you try the {recommended_pose['name']}! "
                         f"The difficulty level of the pose suits {recommended_pose['difficulty']}, "
                         f"the target of the pose is: {recommended_pose['target']}, "
                         f"and it involves the body parts: {', '.join(recommended_pose['body_parts'])}. "
                         f"Practicing this pose will significantly contribute to {recommended_pose['description']}.",
                'recommended_pose': recommended_pose_data
            })

            # IF no recommedn keep message
        try:
            chat_reply = zhipu_model(user_input)
        except Exception as e:
            print(f"Error in zhipu_model: {str(e)}")
            chat_reply = "Sorry, I couldn't generate a response."

            # If no recommendation
        return jsonify({
            'reply': chat_reply,
            'recommended_pose': None 
        })

    except Exception as e:
        print(f"Error in chat_with_user: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/register', methods=['POST'])
def user_register():
    data = request.get_json()
    username = data.get("username")
    print(username)
    # Process the username or authenticate here as needed
    if not username:
        return jsonify({"error": "No username provided"}), 400

    # Check if the username already exists
    user = User.query.filter_by(name=username).first()
    if user:
        return jsonify({"message": f"Welcome back, {username}!"}), 200
    else:
        # Add the new user to the database
        new_user = User(name=username)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": f"New user {username} added to the database."}), 201


if __name__ == '__main__':
    app.run(debug=True, port=8000)

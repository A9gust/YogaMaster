from yoga_database import yoga_poses  # 导入瑜伽姿势数据库
import random

def recommend_pose(level, target):
    # Base on level and aim
    recommended = [
        pose for pose in yoga_poses
        if pose.difficulty == level and any(t in pose.target for t in target)
    ]
    return random.choice(recommended) if recommended else None

if __name__ == "__main__":
    # Output sample
    level_input = "beginner"  
    target_input = ["strength"]

    recommended_pose = recommend_pose(level_input, target_input)

    if recommended_pose:
        print(f"推荐的姿势: {recommended_pose.name}, 难度: {recommended_pose.difficulty}, 描述: {recommended_pose.description}")
    else:
        print("未找到符合条件的姿势。")

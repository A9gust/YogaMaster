import os

class YogaPose:
    def __init__(self, name, difficulty, target, body_parts, image_path, description=None):
        self.name = name  # Name
        self.difficulty = difficulty  # Difficulty level
        self.target = target  # Train target area
        self.body_parts = body_parts  # Human body
        self.image_path = image_path  # Imge path
        self.description = description  # Descripition


base_path = 'images/'


def get_image_path(file_name):
    return os.path.join(base_path, file_name)

# pose database
yoga_poses = [
    YogaPose(
        'Chair Pose',
        'beginner',
        'strength',
        ['legs', 'back'],
        get_image_path('Chair_Pose.jpg'),
        'Strengthens the thighs, calves, and spine while improving balance.'
    ),
    YogaPose(
        'Dolphin Plank Pose',
        'intermediate',
        'core_strength',
        ['core', 'arms'],
        get_image_path('Dolphin Plank Pose.png'),
        'Strengthens the core, shoulders, arms, and legs with a focus on balance.'
    ),
    YogaPose(
        'Downward-facing Dog Pose',
        'beginner',
        'flexibility',
        ['arms', 'legs'],
        get_image_path('Downward-facing Dog Pose.jpg'),
        'Stretches the shoulders, hamstrings, calves, and hands while strengthening the arms and legs.'
    ),
    YogaPose(
        'Fish Pose',
        'beginner',
        'flexibility',
        ['chest', 'neck'],
        get_image_path('Fish Pose.jpg'),
        'Stretches the chest, throat, and abdomen while relieving tension in the upper body.'
    ),
    YogaPose(
        'Goddess Pose',
        'intermediate',
        'strength',
        ['legs', 'hips'],
        get_image_path('Goddess Pose.jpg'),
        'Strengthens the inner thighs, groin, and core, improving flexibility in the hips.'
    ),
    YogaPose(
        'Locust Pose',
        'intermediate',
        'back_strength',
        ['back', 'glutes'],
        get_image_path('Locust Pose.jpg'),
        'Strengthens the muscles of the spine, buttocks, and backs of the arms and legs.'
    ),
    YogaPose(
        'Lord of the Dance Pose',
        'advanced',
        'balance',
        ['legs', 'arms'],
        get_image_path('Lord of the Dance Pose.jpg'),
        'A deep backbend and balance pose that stretches the chest, shoulders, and thighs while improving focus.'
    ),
    YogaPose(
        'Low Lunge Pose',
        'beginner',
        'flexibility',
        ['legs', 'hips'],
        get_image_path('Low Lunge Pose.jpg'),
        'Stretches the hips, groin, and legs while promoting stability and balance.'
    ),
    YogaPose(
        'Seated Forward Bend Pose',
        'beginner',
        'flexibility',
        ['back', 'legs'],
        get_image_path('Seated Forward Bend Pose.jpg'),
        'Stretches the spine, shoulders, and hamstrings while calming the mind.'
    ),
    YogaPose(
        'Side Plank Pose',
        'intermediate',
        'core_strength',
        ['core', 'arms'],
        get_image_path('Side Plank Pose.jpg'),
        'Strengthens the arms, legs, and core while improving balance and stability.'
    ),
    YogaPose(
        'Staff Pose',
        'beginner',
        'posture',
        ['back', 'legs'],
        get_image_path('Staff Pose.jpg'),
        'Improves posture and strengthens the back, arms, and legs while preparing the body for more intense poses.'
    ),
    YogaPose(
        'Tree Pose',
        'beginner',
        'balance',
        ['legs'],
        get_image_path('Tree Pose.jpg'),
        'Improves balance and strengthens the legs, while promoting focus and mental clarity.'
    ),
    YogaPose(
        'Warrior 1 Pose',
        'beginner',
        'strength',
        ['legs', 'arms'],
        get_image_path('Warrior 1 Pose.jpg'),
        'Strengthens the legs, opens the hips, chest, and lungs while improving focus and stamina.'
    ),
    YogaPose(
        'Warrior 2 Pose',
        'beginner',
        'strength',
        ['legs', 'arms'],
        get_image_path('Warrior 2 Pose.jpg'),
        'Strengthens the legs and arms while improving stamina and focus.'
    ),
    YogaPose(
        'Warrior 3 Pose',
        'intermediate',
        'balance',
        ['legs', 'back'],
        get_image_path('Warrior 3 Pose.jpg'),
        'Strengthens the legs, back, and core while improving balance and coordination.'
    ),
    YogaPose(
        'Wide-Angle Seated Forward Bend Pose',
        'intermediate',
        'flexibility',
        ['hips', 'legs'],
        get_image_path('Wide-Angle Seated Forward Bend Pose.jpg'),
        'Stretches the hips, hamstrings, and lower back while promoting relaxation.'
    ),
]

# Recommend function
def recommend_yoga_pose(user_input):
    user_input = user_input.lower()

    # MAPPING
    keyword_to_target = {
        'strength': 'strength',  # Strength
        'flexibility': 'flexibility',  # Flex
        'balance': 'balance',  # Balance
        'core': 'core_strength',  # Core
        'posture': 'posture',  # Posture
        'back': 'back_strength', 
        'spine': 'back_strength',  
        'relaxation': 'relaxation', 
        'arms': 'arms', 
        'legs': 'legs',  
        'hips': 'hips',  
        'glutes': 'glutes',  
        'shoulders': 'shoulders',  
        'neck': 'neck',  
        'chest': 'chest',  
        'hamstrings': 'legs',  
        'quadriceps': 'legs',  
        'calves': 'calves',  
        'feet': 'feet',  
        'wrists': 'wrists',  
        'ankles': 'ankles', 
        'pelvis': 'hips',  
        'abdomen': 'core_strength',  
        'inner thighs': 'inner_thighs', 
        'groin': 'groin',  
        'mind': 'relaxation',  
        'meditation': 'relaxation',  
        'circulation': 'circulation',  
        'shoulder blades': 'shoulders',  
        'spinal': 'back_strength',  
        'mobility': 'flexibility',  
        'lower back': 'back_strength',  
        'upper back': 'back_strength',  
        'lateral': 'lateral_flexibility', 
    }

    # Check key word
    for keyword, target in keyword_to_target.items():
        if keyword in user_input:
            matched_poses = [pose for pose in yoga_poses if target in pose.target or keyword in pose.body_parts]

            if matched_poses:
                # Choose a recommend pose
                recommended_pose = matched_poses[0]  
                return {
                    'name': recommended_pose.name,
                    'description': recommended_pose.description,
                    'image_path': recommended_pose.image_path,
                    'difficulty': recommended_pose.difficulty,
                    'target': recommended_pose.target,
                    'body_parts': recommended_pose.body_parts
                }

    return {
        'name': 'Downward-facing Dog Pose',
        'description': 'A great pose for overall body relaxation.',
        'image_path': 'static/images/Downward-facing Dog Pose.jpg',
        'difficulty': 'beginner',
        'target': 'flexibility',
        'body_parts': ['arms', 'legs']
    }

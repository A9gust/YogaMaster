import pandas as pd
import numpy as np


def calculate_angle(a, b, c):
    ba = a - b
    bc = c - b
    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    angle = np.arccos(cosine_angle)
    return np.degrees(angle)


def calculate_symmetry(left_point, right_point, threshold):
    difference = abs(left_point[0] - right_point[0])  # compare
    return '对称' if difference <= threshold else '不对称'


def calculate_thresholds_for_each_image(left_points, right_points):
    return np.max(np.abs(left_points[:, 0] - right_points[:, 0]))
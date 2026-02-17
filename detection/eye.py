import numpy as np
from scipy.spatial.distance import euclidean

LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]

def eye_aspect_ratio(landmarks, eye_idx, w, h):
    eye = [(int(landmarks[i].x * w), int(landmarks[i].y * h)) for i in eye_idx]
    A = euclidean(eye[1], eye[5])
    B = euclidean(eye[2], eye[4])
    C = euclidean(eye[0], eye[3])
    return (A + B) / (2.0 * C)

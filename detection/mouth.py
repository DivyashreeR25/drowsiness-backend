import numpy as np
from scipy.spatial.distance import euclidean

MOUTH = [13, 14, 78, 308]

def mouth_aspect_ratio(landmarks, w, h):
    p = [(int(landmarks[i].x * w), int(landmarks[i].y * h)) for i in MOUTH]
    vertical = euclidean(p[0], p[1])
    horizontal = euclidean(p[2], p[3])
    return vertical / horizontal

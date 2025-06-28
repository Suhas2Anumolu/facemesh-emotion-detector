import numpy as np
from config import *

def get_coord(landmark, shape):
    return int(landmark.x * shape[0]), int(landmark.y * shape[1])

def distance(p1, p2):
    return np.linalg.norm(np.array(p1) - np.array(p2))

def get_emotion(landmarks, shape):
    mouth_top = get_coord(landmarks[MOUTH_TOP], shape)
    mouth_bottom = get_coord(landmarks[MOUTH_BOTTOM], shape)
    mouth_left = get_coord(landmarks[MOUTH_LEFT], shape)
    mouth_right = get_coord(landmarks[MOUTH_RIGHT], shape)

    left_eye_top = get_coord(landmarks[LEFT_EYE_TOP], shape)
    left_eye_bottom = get_coord(landmarks[LEFT_EYE_BOTTOM], shape)
    right_eye_top = get_coord(landmarks[RIGHT_EYE_TOP], shape)
    right_eye_bottom = get_coord(landmarks[RIGHT_EYE_BOTTOM], shape)

    mouth_open = distance(mouth_top, mouth_bottom)
    mouth_stretch = distance(mouth_left, mouth_right)
    eye_open = (distance(left_eye_top, left_eye_bottom) + distance(right_eye_top, right_eye_bottom)) / 2

    norm_mouth_open = mouth_open / mouth_stretch if mouth_stretch else 0
    norm_eye_open = eye_open / mouth_stretch if mouth_stretch else 0

    if norm_mouth_open > 0.5 and norm_eye_open > 0.2:
        emotion = "Surprised"
    elif norm_mouth_open < 0.2 and norm_eye_open < 0.1:
        emotion = "Sad"
    elif mouth_left[1] < mouth_right[1] - 3:
        emotion = "Happy"
    elif norm_eye_open < 0.1 and norm_mouth_open < 0.2:
        emotion = "Angry"
    else:
        emotion = "Neutral"

    debug_data = f"mouth_open={norm_mouth_open:.3f}, mouth_stretch={mouth_stretch:.3f}, eye_open={norm_eye_open:.3f}"
    return emotion, debug_data

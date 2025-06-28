import cv2

def draw_avatar(canvas, emotion):
    color = {
        "Happy": (0, 255, 0),
        "Sad": (255, 0, 0),
        "Angry": (0, 0, 255),
        "Surprised": (255, 255, 0),
        "Neutral": (200, 200, 200)
    }.get(emotion, (255, 255, 255))

    center = (320, 240)
    cv2.circle(canvas, center, 100, color, 2)

    cv2.circle(canvas, (280, 210), 10, color, -1)
    cv2.circle(canvas, (360, 210), 10, color, -1)

    if emotion == "Happy":
        cv2.ellipse(canvas, (320, 280), (40, 20), 0, 0, 180, color, 3)
    elif emotion == "Sad":
        cv2.ellipse(canvas, (320, 300), (40, 20), 0, 0, -180, color, 3)
    elif emotion == "Surprised":
        cv2.circle(canvas, (320, 280), 15, color, 2)
    else:
        cv2.line(canvas, (280, 280), (360, 280), color, 3)

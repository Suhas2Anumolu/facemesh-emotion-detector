import cv2
import time
import numpy as np
import mediapipe as mp
from utils import get_emotion
from avatar import draw_avatar

mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

cap = cv2.VideoCapture(0)
prev_time = 0

with mp_face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
) as face_mesh:

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            continue

        frame = cv2.flip(frame, 1)
        h, w, _ = frame.shape
        blank = np.zeros_like(frame)

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb)

        if results.multi_face_landmarks:
            landmarks = results.multi_face_landmarks[0]
            emotion, debug = get_emotion(landmarks.landmark, (w, h))

            mp_drawing.draw_landmarks(
                blank,
                landmarks,
                mp_face_mesh.FACEMESH_TESSELATION,
                landmark_drawing_spec=None,
                connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_tesselation_style()
            )

            cv2.putText(blank, f"{emotion.upper()}  ????", (30, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 3)

            print(f"[DEBUG] {debug}")

            # Optional cartoon face
            draw_avatar(blank, emotion)

        curr_time = time.time()
        fps = int(1 / (curr_time - prev_time)) if prev_time else 0
        prev_time = curr_time
        cv2.putText(blank, f"FPS: {fps}", (30, 90),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.imshow("Avatar Emotion Mesh", blank)
        if cv2.waitKey(5) & 0xFF == 27:
            break

cap.release()
cv2.destroyAllWindows()

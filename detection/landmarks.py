import cv2
import mediapipe.python.solutions.face_mesh as face_mesh

class FaceLandmarks:
    def __init__(self):
        self.face_mesh = face_mesh.FaceMesh(
            static_image_mode=False,
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )

    def get_landmarks(self, frame):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = self.face_mesh.process(rgb)
        if result.multi_face_landmarks:
            return result.multi_face_landmarks[0].landmark
        return None

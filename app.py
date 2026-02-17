from flask import Flask, request, jsonify
from flask_cors import CORS
import base64
import cv2
import numpy as np

from detection.landmarks import FaceLandmarks
from detection.eye import LEFT_EYE, RIGHT_EYE, eye_aspect_ratio
from detection.mouth import mouth_aspect_ratio
from detection.head_pose import head_down
from detection.drowsiness import DrowsinessDetector

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


# ---------------- GLOBAL STATE ----------------
running = False

landmark_detector = FaceLandmarks()
drowsy_detector = DrowsinessDetector()

# ---------------- HELPERS ----------------
def decode_base64_image(data):
    try:
        if "," in data:
            data = data.split(",")[1]

        img_bytes = base64.b64decode(data, validate=True)
        np_arr = np.frombuffer(img_bytes, np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        if img is None:
            return None

        return img
    except Exception as e:
        print("Base64 decode error:", e)
        return None


# ---------------- API ENDPOINTS ----------------

@app.route("/start", methods=["POST"])
def start():
    global running
    running = True
    return jsonify({"status": "detection started"}), 200


@app.route("/stop", methods=["POST"])
def stop():
    global running
    running = False
    return jsonify({"status": "detection stopped"}), 200


@app.route("/status", methods=["GET"])
def status():
    return jsonify({"running": running}), 200


@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json(silent=True)
    if not data or "image" not in data:
        return jsonify({"error": "image not provided"}), 400

    frame = decode_base64_image(data["image"])
    if frame is None:
        return jsonify({"error": "invalid image format"}), 400

    landmarks = landmark_detector.get_landmarks(frame)
    if landmarks is None:
        return jsonify({"status": "no_face_detected"}), 200

    h, w = frame.shape[:2]

    try:
        ear_left = eye_aspect_ratio(landmarks, LEFT_EYE, w, h)
        ear_right = eye_aspect_ratio(landmarks, RIGHT_EYE, w, h)
        ear = float((ear_left + ear_right) / 2.0)

        mar = float(mouth_aspect_ratio(landmarks, w, h))
        head = bool(head_down(landmarks))

    except Exception as e:
        print("Landmark processing error:", e)
        return jsonify({"status": "processing_error"}), 200

    drowsy = bool(drowsy_detector.check(ear, mar, head))

    return jsonify({
        "status": "drowsy" if drowsy else "alert",
        "eye_closed": bool(ear < 0.25),
        "yawning": bool(mar > 0.75),
        "head_down": bool(head)
    }), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


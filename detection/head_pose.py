def head_down(landmarks):
    nose_y = landmarks[1].y
    chin_y = landmarks[152].y

    # Head considered down only if chin moves significantly closer to nose
    return (chin_y - nose_y) < 0.10

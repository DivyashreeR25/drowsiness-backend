from config import *
from utils.timer import Timer

class DrowsinessDetector:
    def __init__(self):
        self.eye_timer = Timer()
        self.mouth_timer = Timer()
        self.head_timer = Timer()

    def check(self, ear, mar, head_down):
        drowsy = False

        # ---- EYES CLOSED ----
        if ear < EYE_AR_THRESH:
            self.eye_timer.start()
            if self.eye_timer.elapsed() >= EYE_AR_TIME:
                drowsy = True
        else:
            self.eye_timer.reset()

        # ---- YAWNING ----
        if mar > MOUTH_AR_THRESH:
            self.mouth_timer.start()
            if self.mouth_timer.elapsed() >= 1.5:
                drowsy = True
        else:
            self.mouth_timer.reset()

        # ---- HEAD DOWN ----
        if head_down:
            self.head_timer.start()
            if self.head_timer.elapsed() >= HEAD_DOWN_TIME:
                drowsy = True
        else:
            self.head_timer.reset()

        return drowsy

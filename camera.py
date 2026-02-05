import cv2

class Camera:
    def __init__(self, cam_id=0):
        self.cap = cv2.VideoCapture(cam_id)

    def read(self):
        ret, frame = self.cap.read()
        if not ret:
            raise RuntimeError("Failed to read camera frame")
        return frame

    def release(self):
        self.cap.release()
        cv2.destroyAllWindows()

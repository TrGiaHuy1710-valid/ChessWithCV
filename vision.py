import cv2
import numpy as np

class MoveDetector:
    def __init__(self, board_mapper):
        self.mapper = board_mapper
        self.prev = None

    def record(self, frame):
        self.prev = frame.copy()

    def detect(self, frame):
        if self.prev is None:
            return None

        g1 = cv2.cvtColor(self.prev, cv2.COLOR_BGR2GRAY)
        g2 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        diff = cv2.absdiff(g1, g2)
        _, diff = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)

        diff = cv2.dilate(diff, None, iterations=4)
        diff = cv2.erode(diff, None, iterations=6)

        contours, _ = cv2.findContours(
            diff, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        if len(contours) < 2:
            return None

        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:2]
        squares = []

        for c in contours:
            x, y, w, h = cv2.boundingRect(c)
            cx, cy = x + w // 2, y + int(0.7 * h)
            sq = self.mapper.find_square(cx, cy)
            if sq:
                squares.append(sq)

        if len(squares) == 2:
            return squares[0] + squares[1]

        return None

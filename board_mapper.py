import json
import cv2
import numpy as np

class BoardMapper:
    def __init__(self, json_path="sqdict.json"):
        with open(json_path, "r") as f:
            self.sq_points = json.load(f)

    def find_square(self, x, y):
        for sq, pts in self.sq_points.items():
            poly = np.array(pts, np.int32)
            if cv2.pointPolygonTest(poly, (x, y), False) > 0:
                return sq
        return None

    def draw_outlines(self, frame, show_text=False):
        for sq, pts in self.sq_points.items():
            poly = np.array(pts, np.int32)
            cv2.polylines(frame, [poly], True, (255, 255, 255), 1)
            if show_text:
                x, y, w, h = cv2.boundingRect(poly)
                cv2.putText(frame, sq, (x, y + 15),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 1)

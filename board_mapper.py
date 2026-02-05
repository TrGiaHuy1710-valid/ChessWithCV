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

def test_board_mapper(image_path , json_path="sqdict.json"):
    mapper = BoardMapper()

    image = cv2.imread(image_path)
    assert image is not None , "Image is none"

    display_img = image.copy()

    mapper.draw_outlines(display_img, show_text=True)

    def on_mouse_click(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            square = mapper.find_square(x, y)
            if square:
                print(f"You clicked square {square} (cordinate: {x}, {y})")
            else:
                print(f"Click outside square {square} (cordinate: {x}, {y})")

    cv2.namedWindow("Test Board mapper")
    cv2.setMouseCallback("Test Board mapper", on_mouse_click)

    print("Hướng dẫn: Click chuột trái vào các ô trên ảnh để xem tên ô.")
    print("Nhấn ESC bất kỳ để thoát.")

    while True:
        cv2.imshow("Test Board mapper", display_img)
        if cv2.waitKey(1) & 0xFF == 27:
            break

    cv2.destroyAllWindows()

if __name__ == '__main__':
    test_board_mapper("assets/images/images.jpg", "sqdict.json")

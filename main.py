import cv2
import chess

from camera import Camera
from board_mapper import BoardMapper
from vision import MoveDetector
from chess_engine import StockfishEngine
from visualizer import ChessVisualizer

ENGINE_PATH = "E:\Python_Project\Realsense\CVchess\G7_CVChess\stockfish-windows-x86-64-avx2\stockfish\stockfish-windows-x86-64-avx2.exe"

def main():
    # video_path = r"E:\Python_Project\Realsense\CVchess\G7_CVChess\image\chess_video.mp4"
    cam = Camera(1)
    mapper = BoardMapper("sqdict.json")
    detector = MoveDetector(mapper)
    engine = StockfishEngine(ENGINE_PATH)
    viz = ChessVisualizer()

    board = chess.Board()
    viz.show(board)

    print("Press 'r' to record move, 'q' to quit")

    while not board.is_game_over():
        frame = cam.read()
        mapper.draw_outlines(frame)
        cv2.imshow("Camera", frame)

        key = cv2.waitKey(1) & 0xFF

        if key == ord('r'):
            detector.record(frame)
            print("Recorded start position")

            cv2.waitKey(800)  # wait for move
            frame2 = cam.read()

            move = detector.detect(frame2)
            if move:
                print("Detected move:", move)
                board.push_uci(move)
                viz.show(board, move)

                ai_move = engine.best_move(board)
                board.push(ai_move)
                viz.show(board, ai_move.uci())
            else:
                print("Move not detected")

        if key == ord('q'):
            break

    engine.close()
    cam.release()

if __name__ == "__main__":
    main()

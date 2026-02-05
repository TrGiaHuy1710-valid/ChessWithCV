import chess
import chess.engine

class StockfishEngine:
    def __init__(self, engine_path):
        self.engine = chess.engine.SimpleEngine.popen_uci(engine_path)

    def best_move(self, board, time_limit=0.5):
        result = self.engine.play(board, chess.engine.Limit(time=time_limit))
        return result.move

    def close(self):
        self.engine.quit()

import chess
import chess.engine

class ChessGame:
    def __init__(self):
        self.board = chess.Board()
        self.move_history = []
        
    def reset(self):
        self.board = chess.Board()
        self.move_history = []
        
    def get_board(self):
        board_array = []
        for rank in range(8):
            row = []
            for file in range(8):
                square = chess.square(file, 7-rank)
                piece = self.board.piece_at(square)
                if piece is None:
                    row.append('.')
                else:
                    row.append(piece.symbol())
            board_array.append(row)
        return board_array
        
    def get_fen(self):
        return self.board.fen()
        
    def get_legal_moves(self):
        return [move.uci() for move in self.board.legal_moves]
        
    def make_move(self, move_str):
        try:
            move = chess.Move.from_uci(move_str)
            if move in self.board.legal_moves:
                self.board.push(move)
                self.move_history.append(move_str)
                return True
            return False
        except:
            return False
            
    def is_game_over(self):
        return self.board.is_game_over()
        
    def is_check(self):
        return self.board.is_check()
        
    def get_game_result(self):
        if self.board.is_checkmate():
            if self.board.turn == chess.WHITE:
                return "Black wins by checkmate"
            else:
                return "White wins by checkmate"
        elif self.board.is_stalemate():
            return "Draw by stalemate"
        elif self.board.is_insufficient_material():
            return "Draw by insufficient material"
        elif self.board.is_seventyfive_moves():
            return "Draw by 75-move rule"
        elif self.board.is_fivefold_repetition():
            return "Draw by fivefold repetition"
        else:
            return "Game continues"
            
    @property
    def current_turn(self):
        return 'white' if self.board.turn else 'black'
        
    def get_move_history(self):
        return self.move_history.copy()
        
    def get_board_notation(self):
        return str(self.board)
        
    def get_pgn(self):
        game = chess.pgn.Game()
        node = game
        
        temp_board = chess.Board()
        for move_str in self.move_history:
            move = chess.Move.from_uci(move_str)
            node = node.add_variation(move)
            temp_board.push(move)
            
        return str(game)

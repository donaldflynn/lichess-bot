from typing import Optional
import logging
import chess
from lib import model
import random

logger = logging.getLogger(__name__)


value_mapping = {
    chess.PAWN: 1,
    chess.KNIGHT: 3,
    chess.BISHOP: 3,
    chess.ROOK: 5,
    chess.QUEEN: 8,
    chess.KING: 0,
}

color_mapping = {
    chess.WHITE: 1,
    chess.BLACK: -1
}


class TimeManager:
    def __init__(self, board: chess.Board, game: model.Game):
        self.game_state = _GameState(board, game)

    def get_initial_time(self) -> float:
        """Returns actual thinking time of the move"""
        my_time, my_inc = self.game_state.time_left
        if my_time < 60:
            return 0.5
        else:
            return 1

    def get_pause_time(self, move: chess.Move) -> float:
        """Returns fake thinking time after making the move"""
        my_time, my_inc = self.game_state.time_left
        if self.game_state.move_number < 10:
            return 0
        if my_time < 10:
            return 0
        if self.game_state.is_recapture(move):
            return 0

        elif 10 <= my_time < 60:
            return random.uniform(0, self._get_complexity_measure())
        elif my_time >= 60:
            # https://www.desmos.com/calculator/f5cgemje2s
            # Random weight between 0 and 1 weighted towards the bottom, but with a long tail
            rand_weight = min(random.lognormvariate(-1, 5), 1)
            return rand_weight * 15 * self._get_complexity_measure()

    def _get_complexity_measure(self) -> float:
        """Returns a value between 0 and 1 corresponding roughly to how complex the game is"""
        complexity_percent = 0

        # 50 Points from how many legal moves there are:
        complexity_percent += min(self.game_state.get_legal_moves_count() * 1.5, 50)

        # 25 Points for if classified as middlegame instead of endgame:
        if not self.game_state.is_endgame():
            complexity_percent += 25

        # 25 Points for if the game is equal or not
        if self.game_state.is_equal():
            complexity_percent += 25

        return complexity_percent / 100


class _LastPosition:
    def __init__(self, board: chess.Board):
        self.board = board
        self.last_move: Optional[chess.Move] = None

    def __enter__(self):
        """
        It's up to the caller to ensure that there is a previous move.
        """
        self.last_move = self.board.pop()
        return self.board, self.last_move

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.board.push(self.last_move)


class _GameState:
    def __init__(self, board: chess.Board, game: model.Game):
        self.board = board
        self.game = game
        self._is_white = game.my_color == "white"

    def is_endgame(self) -> bool:
        has_white_queen = len(self.board.pieces(chess.QUEEN, chess.WHITE)) == 0
        has_black_queen = len(self.board.pieces(chess.QUEEN, chess.BLACK)) == 0
        if has_white_queen and has_black_queen:
            return False
        if self.total_material_value > 20:
            return False

    def is_equal(self) -> bool:
        return abs(self.material_diff) <= 5

    def is_recapture(self, current_move: chess.Move) -> bool:
        if self.is_first_move:
            return False
        with _LastPosition(self.board) as context:
            last_pos, last_move = context
            return (
                    current_move.to_square == last_move.to_square and
                    last_pos.piece_at(last_move.to_square) is not None
            )

    def get_legal_moves_count(self) -> int:
        return self.board.legal_moves.count()

    @property
    def time_left(self) -> tuple[float, float]:
        return self.game.my_remaining_time().total_seconds(), self.game.clock_increment

    @property
    def material_diff(self):
        return sum(
            value_mapping[piece.piece_type] * color_mapping[piece.color]
            for square in chess.SQUARES
            if (piece := self.board.piece_at(square)) is not None
        )

    @property
    def total_material_value(self):
        return sum(
            value_mapping[piece.piece_type]
            for square in chess.SQUARES
            if (piece := self.board.piece_at(square)) is not None
        )

    @property
    def relative_material_diff(self):
        return self.material_diff if self._is_white else -self.material_diff

    @property
    def is_first_move(self):
        return self.board.move_stack == []

    @property
    def move_number(self):
        return self.board.fullmove_number


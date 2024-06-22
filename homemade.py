"""
Some example classes for people who want to create a homemade bot.

With these classes, bot makers will not have to implement the UCI or XBoard interfaces themselves.
"""
import chess
from chess.engine import PlayResult, Limit
import chess.engine
import random
from lib.engine_wrapper import MinimalEngine
from lib.types import MOVE, HOMEMADE_ARGS_TYPE
import logging


# Use this logger variable to print messages to the console or log files.
# logger.info("message") will always print "message" to the console or log file.
# logger.debug("message") will only print "message" if verbose logging is enabled.
logger = logging.getLogger(__name__)


LEELA_PATH = "/app/engines/lc0"
STOCKFISH_PATH = "/app/engines/stockfish"

MAIA_CANDIDATE_MOVES = 3

class ExampleEngine(MinimalEngine):
    """An example engine that all homemade engines inherit."""

    pass


class Hybrid(ExampleEngine):
    def __init__(self, *args, **kwargs):
        super(Hybrid, self).__init__(*args, **kwargs)
        self._leela_engine = chess.engine.SimpleEngine.popen_uci(LEELA_PATH)
        self._stockfish_engine = chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH)
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Wrap the exit method of ExampleEngine to ensure we exit the engines properly in case of an
        exception etc
        """
        self._leela_engine.__exit__(exc_type, exc_val, exc_tb)
        self._stockfish_engine.__exit__(exc_type, exc_val, exc_tb)
        super(Hybrid, self).__exit__(exc_type, exc_val, exc_tb)

    def search(self, board: chess.Board, *args: HOMEMADE_ARGS_TYPE) -> PlayResult:
        info_list = self._leela_engine.analyse(board, chess.engine.Limit(time=2), multipv=MAIA_CANDIDATE_MOVES)
        moves_list = [info['pv'][0] for info in info_list]
        logger.info("Candidate moves received from maia: " + ", ".join([str(move) for move in moves_list]))
        play_result = self._stockfish_engine.play(board, chess.engine.Limit(time=0.1), root_moves=moves_list)
        logger.info("Final move decided from stockfish: %s", str(play_result.move))
        return play_result


# Bot names and ideas from tom7's excellent eloWorld video

class RandomMove(ExampleEngine):
    """Get a random move."""

    def search(self, board: chess.Board, *args: HOMEMADE_ARGS_TYPE) -> PlayResult:
        """Choose a random move."""
        return PlayResult(random.choice(list(board.legal_moves)), None)


class Alphabetical(ExampleEngine):
    """Get the first move when sorted by san representation."""

    def search(self, board: chess.Board, *args: HOMEMADE_ARGS_TYPE) -> PlayResult:
        """Choose the first move alphabetically."""
        moves = list(board.legal_moves)
        moves.sort(key=board.san)
        return PlayResult(moves[0], None)


class FirstMove(ExampleEngine):
    """Get the first move when sorted by uci representation."""

    def search(self, board: chess.Board, *args: HOMEMADE_ARGS_TYPE) -> PlayResult:
        """Choose the first move alphabetically in uci representation."""
        moves = list(board.legal_moves)
        moves.sort(key=str)
        return PlayResult(moves[0], None)


class ComboEngine(ExampleEngine):
    """
    Get a move using multiple different methods.

    This engine demonstrates how one can use `time_limit`, `draw_offered`, and `root_moves`.
    """

    def search(self, board: chess.Board, time_limit: Limit, ponder: bool, draw_offered: bool, root_moves: MOVE) -> PlayResult:
        """
        Choose a move using multiple different methods.

        :param board: The current position.
        :param time_limit: Conditions for how long the engine can search (e.g. we have 10 seconds and search up to depth 10).
        :param ponder: Whether the engine can ponder after playing a move.
        :param draw_offered: Whether the bot was offered a draw.
        :param root_moves: If it is a list, the engine should only play a move that is in `root_moves`.
        :return: The move to play.
        """
        if isinstance(time_limit.time, int):
            my_time = time_limit.time
            my_inc = 0
        elif board.turn == chess.WHITE:
            my_time = time_limit.white_clock if isinstance(time_limit.white_clock, int) else 0
            my_inc = time_limit.white_inc if isinstance(time_limit.white_inc, int) else 0
        else:
            my_time = time_limit.black_clock if isinstance(time_limit.black_clock, int) else 0
            my_inc = time_limit.black_inc if isinstance(time_limit.black_inc, int) else 0

        possible_moves = root_moves if isinstance(root_moves, list) else list(board.legal_moves)

        if my_time / 60 + my_inc > 10:
            # Choose a random move.
            move = random.choice(possible_moves)
        else:
            # Choose the first move alphabetically in uci representation.
            possible_moves.sort(key=str)
            move = possible_moves[0]
        return PlayResult(move, None, draw_offered=draw_offered)
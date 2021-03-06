from typing import Optional

from .boardstate import BoardState
from itertools import product

# class PositionEvaluation:


def PositionEvaluation(Board: BoardState) -> int:
    # for now it's semi dump version
    if Board is None:
        return -100500
    black_count = 0
    board_value = 0
    for y, x in product(range(8), range(8)):
        board_value += Board.board[y, x]
        if Board.board[y, x] < 0:
            black_count += 1
    if black_count == 0:
        board_value = 100500  # max board val
    return board_value


class AI:
    def __init__(self, search_depth: int):
        self.depth: int = search_depth

    def next_move(self, Board: BoardState, current_depth: int = -1, player: int = 1):
        if current_depth == -1:
            current_depth = self.depth
        if current_depth == 0:
            return Board if player == 1 else Board.inverted()

        (possible_pieces, attack_flag) = Board.get_possible_piece()
        if len(possible_pieces) == 0:
            if player == 1:
                return None
            else:
                return Board.inverted()

        best_board = BoardState()
        best_eval = -100500
        for pos in possible_pieces:
            for next_board in Board.get_possible_turn_iterator(
                    pos[0], pos[1], attack_flag):
                if player == 1:
                    cur_board = self.next_move(
                        next_board.inverted(), current_depth, -1)
                else:
                    cur_board = self.next_move(
                        next_board.inverted(), current_depth - 1, 1)

                cur_eval = PositionEvaluation(cur_board)
                if cur_eval > best_eval:
                    best_board = next_board
                    best_eval = cur_eval
        if player == 1:
            return best_board
        else:
            return best_board.inverted()

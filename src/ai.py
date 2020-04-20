from typing import Optional

from .boardstate import BoardState
from itertools import product

#class PositionEvaluation:
def PositionEvaluation(Board: BoardState) -> int:
    # for now it's semi dump version
    if Board == None:
        return -100500
    black_count = 0
    board_value = 0
    for y, x in product(range(8), range(8)):
        board_value += Board.board[y, x]
        if Board.board[y, x] < 0:
            black_count += 1
    if black_count == 0:
        board_value = 100500 # max board val
    return board_value


class AI:
    def __init__(self, search_depth: int):
        self.depth: int = search_depth
    

    def simple_next_move(self, Board: BoardState) -> Optional[BoardState]:
        best_board = BoardState()
        cur_eval = -100500 #PositionEvaluation(best_board)
        (possible_pieces, attack_flag) = Board.get_possible_piece()
        if len(possible_pieces) == 0:
            return None
        for pos in possible_pieces:
            for next_board in Board.get_possible_turn_iterator(pos[0], pos[1], attack_flag):
                next_eval = PositionEvaluation(next_board)
                if next_eval > cur_eval:
                    next_eval = cur_eval
                    best_board = next_board.copy()
        return best_board
        

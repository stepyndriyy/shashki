from itertools import product
import numpy as np
from typing import Optional, List


class BoardState:
    def __init__(self, board: np.ndarray = np.zeros((8,8), dtype=np.int8), current_player: int = 1, ate_pieces: np.ndarray = np.zeros((8, 8), dtype=np.int8)):
        self.board: np.ndarray = board
        self.ate_pieces: np.ndarray=ate_pieces
        self.current_player: int = current_player

    def inverted(self) -> 'BoardState':
        return BoardState(board=self.board[::-1, ::-1] * -1, current_player=self.current_player * -1)

    def copy(self) -> 'BoardState':
        return BoardState(self.board.copy(), self.current_player, self.ate_pieces)
    
    def delete_ate_pieces(self):
        for x, y in product(range(8), range(8)):
            if self.ate_pieces[y, x] == 1:
                self.board[y, x] = 0
                self.ate_pieces[y, x] = 0

    def max_in_ate_pieces(self) -> int:
        ans = 0
        for x, y in product(range(8), range(8)):
            ans = max(ans, self.ate_pieces[y, x])
        return ans

    def get_possible_moves(self, from_y, from_x, only_eating_flag: bool = False) -> List['BoardState']:
        if self.board[from_y, from_x] == 0: 
            return []
        
        answer = list()
        if self.board[from_y, from_x] == 1: 
            if not only_eating_flag:
                if from_y - 1 >= 0:
                    for cur_x in range(from_x - 1, from_x + 2, 2):
                        if cur_x >= 0 and cur_x < 8 and self.board[from_y - 1, cur_x] == 0:
                            answer.append((from_y - 1, cur_x))
            else:
                for dy in range(-1, 2, 2):
                    for dx in range(-1, 2, 2):
                        to_y = from_y + dy
                        to_x = from_x + dx
                        if to_y + dy < 0 or to_y + dy >= 8 or to_x + dx < 0 or to_x + dx >= 8:
                            continue
                        if self.board[to_y, to_x] < 0 and self.board[to_y + dy, to_x + dx] == 0 and self.ate_pieces[to_y, to_x] == 0: 
                            answer.append((to_y + dy, to_x + dx))
        
        if self.board[from_y, from_x] == 2:
            for dx in range(-1, 2, 2):
                for dy in range(-1, 2, 2):
                    enemy_on_line = 0 # cnt of enemy on line
                    to_x = from_x 
                    to_y = from_y
                    while (to_x + dx  >= 0 and to_x + dx < 8) and (to_y + dy >=  0 and to_y + dy < 8):
                        to_x += dx
                        to_y += dy
                        if self.board[to_y, to_x] > 0 or self.ate_pieces[to_y, to_x] == 1: # if we meet our piece or if piece already dead
                            break
                    
                        if self.board[to_y, to_x] < 0:
                            enemy_on_line += 1
                            if enemy_on_line >= 2:
                                break
                            continue

                        if not only_eating_flag and self.board[to_y, to_x] == 0 and enemy_on_line == 0:
                            answer.append((to_y, to_x))

                        if only_eating_flag and self.board[to_y, to_x] == 0 and enemy_on_line == 1: 
                            answer.append((to_y, to_x))

                        if enemy_on_line == 1:
                            break 
        return answer 
    
    def mark_enemy_in_between(self, from_y, from_x, to_y, to_x, MARK : int = 1) -> bool:
        dy = 1 if to_y > from_y else -1
        dx = 1 if to_x > from_x else -1
        cur_x = from_x + dx 
        cur_y = from_y + dy
        while cur_x * dx > from_x * dx and cur_x * dx < to_x * dx and cur_y * dy > from_y * dy and cur_y * dy < to_y * dy:            
            if self.board[cur_y, cur_x] < 0:
                self.ate_pieces[cur_y, cur_x] = MARK
                return True
            cur_x += dx
            cur_y += dy
        return False

    def get_possible_piece(self):
        answer = []
        for y, x in product(range(8), range(8)):
            for piece in self.get_possible_moves(y, x, True):
                if self.mark_enemy_in_between(y, x, piece[0], piece[1], 0):
                    answer.append((y, x))
        if len(answer) > 0:
            return (answer, True)
        for y, x in product(range(8), range(8)):
            if self.board[y, x] > 0:
                answer.append((y, x))
        return (answer, False)

    def do_move(self, from_x, from_y, to_x, to_y, current_piece) -> Optional['BoardState']:
        """
        :return: new BoardState or None for invalid move
        """
        if from_x == to_x and from_y == to_y:
            return None #invalid move

        if (to_x + to_y) % 2 == 0:
            return None
        
        if not (from_y, from_x) in self.get_possible_piece()[0]:
            return None
        
        if current_piece != None and (current_piece[0] != from_x or current_piece[1] != from_y):
            return None
        
        if current_piece != None and ((not (to_y, to_x) in self.get_possible_moves(from_y, from_x, True) or self.max_in_ate_pieces() == 0)):
            return None
        elif current_piece == None:
            possible_kills = self.get_possible_moves(from_y, from_x, True)
            if len(possible_kills) != 0 and not (to_y, to_x) in possible_kills:
                return None
            if len(possible_kills) == 0 and not (to_y, to_x) in self.get_possible_moves(from_y, from_x):
                return None

       
        result = self.copy()
        
        result.mark_enemy_in_between(from_y, from_x, to_y, to_x)
        
        result.board[to_y, to_x] = result.board[from_y, from_x]
        result.board[from_y, from_x] = 0
    
        if to_y == 0:
            result.board[to_y, to_x] = 2

        return result

    def get_white_and_black_count(self) -> list:
        white_count = 0
        black_count = 0
        for y, x in product(range(8), range(8)):
            if self.board[y, x] > 0:
                white_count += 1
            if self.board[y, x] < 0:
                black_count += 1
        return [white_count, black_count]
    
    def _get_next_possible_attack_iterator(self, from_y, from_x):
        possible_moves = self.get_possible_moves(from_y, from_x, True)
        if len(possible_moves) == 0:
            self.delete_ate_pieces()
            yield self.copy()
        else:
            for (to_y, to_x) in possible_moves:
                answer = self.do_move(from_x, from_y, to_x, to_y, None)
                for next_board in answer._get_next_possible_attack_iterator(to_y, to_x):
                    #next_board.delete_ate_pieces()
                    yield next_board

    def get_possible_turn_iterator(self, from_y, from_x, attack_flag=False):
        if not attack_flag:
            for (to_y, to_x) in self.get_possible_moves(from_y, from_x):
                answer = self.do_move(from_x, from_y, to_x, to_y, None)
                answer.delete_ate_pieces()
                yield answer
        else: 
            for next_board in self._get_next_possible_attack_iterator(from_y, from_x):
                yield next_board
    
    @property
    def is_game_finished(self) -> bool:
        cnt = self.get_white_and_black_count()   
        if cnt[0] == 0 or cnt[1] == 0:
            return True
        return False

    @property
    def get_winner(self) -> Optional[int]:
        if not self.is_game_finished:
            return None
        cnt = self.get_white_and_black_count()
        return (1 if cnt[1] == 0 else -1)

    @staticmethod
    def initial_state() -> 'BoardState':
        board = np.zeros(shape=(8, 8), dtype=np.int8)
        for y in range(8):
            if y > 2 and y < 5:
                continue
            for x in range(1 if y % 2 == 0 else 0, 8, 2):
                board[y, x] = -1 if y < 3 else 1
                    
        return BoardState(board, 1)

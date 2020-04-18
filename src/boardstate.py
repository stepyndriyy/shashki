from itertools import product
import numpy as np
from typing import Optional, List


class BoardState:
    def __init__(self, board: np.ndarray, current_player: int = 1):
        self.board: np.ndarray = board
        self.current_player: int = current_player
        # print(board)

    def inverted(self) -> 'BoardState':
        return BoardState(board=self.board[::-1, ::-1] * -1, current_player=self.current_player * -1)

    def copy(self) -> 'BoardState':
        return BoardState(self.board.copy(), self.current_player)

    def get_possible_moves(self, from_y, from_x) -> List['BoardState']:
        if self.board[from_y, from_x] == 0: 
            return []
        
        answer = list()
        if self.board[from_y, from_x] == 1 and from_y - 1 >= 0:
            for dx in range(-1, 2, 2):
                to_y = from_y - 1
                to_x =  from_x + dx
                if to_x < 0 or to_x >= 8:
                    continue
                
                #check if empty plate
                if self.board[to_y, to_x] == 0:
                    answer.append((to_y, to_x))
                
                #check if enemy on plate
                if self.board[to_y, to_x] < 0:
                    to_x += dx
                    to_y += -1
                    if to_x < 0 or to_x >= 8 or to_y < 0:
                        continue
                    if self.board[to_y, to_x] == 0:
                        answer.append((to_y, to_x))
  
        
        if self.board[from_y, from_x] == 2:
            for dx in range(-1, 2, 2):
                for dy in range(-1, 2, 2):    
                    enemy_on_line = 0 # cnt of enemy on line
                    to_x = from_x + dx
                    to_y = from_y + dy
                    while (to_x >= 0 and to_x < 8) and (to_y >=  0 and to_y < 8):
                        if enemy_on_line > 1:
                            break

                        if self.board[to_y, to_x] > 0: # if we meet our piece
                            break
                    
                        if self.board[to_y, to_x] < 0:
                            enemy_on_line += 1

                        if self.board[to_y, to_x] == 0:
                            answer.append((to_y, to_x))
                        
                        to_x += dx
                        to_y += dy
    
        return answer 


    def delete_enemy_in_between(self, from_y, from_x, to_y, to_x):
        dy = 1 if to_y > from_y else -1
        dx = 1 if to_x > from_x else -1
        cur_x = from_x + dx 
        cur_y = from_y + dy
        while cur_x * dx > from_x * dx and cur_x * dx < to_x * dx and cur_y * dy > from_y * dy and cur_y * dy < to_y * dy:            
            if self.board[cur_y, cur_x] < 0:
                self.board[cur_y, cur_x] = 0
            cur_x += dx
            cur_y += dy


    def do_move(self, from_x, from_y, to_x, to_y) -> Optional['BoardState']:
        """
        :return: new BoardState or None for invalid move
        """
        #print(from_y, from_x, self.board[from_y, from_x])
        if from_x == to_x and from_y == to_y:
            return None #invalid move

        if (to_x + to_y) % 2 == 0:
            return None

        if not (to_y, to_x) in BoardState.get_possible_moves(self, from_y, from_x):
            return None

        
        result = self.copy()
        
        result.delete_enemy_in_between(from_y, from_x, to_y, to_x)
        
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

        board[7, 0] = 1  # шашка первого игрока
        board[6, 1] = 2  # дамка первого игрока
        board[0, 1] = -1  # шашка противника

        return BoardState(board, 1)

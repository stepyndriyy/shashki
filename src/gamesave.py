from .boardstate import BoardState
from os import remove

class Gamesave:
    def __init__(self, name: str):
        self.filename = name
   
    def copy_game(self, other):
        from_ = open(other.filename, 'r')
        to = open(self.filename, 'w')
        for line in from_:
            to.write(line)
    
    def delete_save(self):
        remove(self.filename)

    def write_save(self, Board : BoardState):
        gamesave = open(self.filename, 'w')
        for y in range(8):
            for x in range(8):
                gamesave.write(str(Board.board[y, x]) + ' ')
            gamesave.write('\n')
        
    def open_save(self) -> BoardState:
        gamesave = open(self.filename, 'r')
        Board = BoardState()
        y = 0
        for line in gamesave:
            line = list(int(x) for x in line.split())
            for x in range(8):
                Board.board[y, x] = line[x]
            y += 1
        return Board 

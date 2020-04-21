from itertools import product

import pygame
from pygame import Surface

from src.ai import AI, PositionEvaluation
from src.boardstate import BoardState


def draw_board(screen: Surface, pos_x: int, pos_y: int, elem_size: int, board: BoardState, GreenPlates : list):
    dark = (0, 0, 0)
    white = (200, 200, 200)
    green = (0, 128, 0)

    for y, x in product(range(8), range(8)):
        color = white if (x + y) % 2 == 0 else dark
        if (y, x) in GreenPlates:
            color = green
        position = pos_x + x * elem_size, pos_y + y * elem_size, elem_size, elem_size
        pygame.draw.rect(screen, color, position)

        figure = board.board[y, x]

        if figure == 0:
            continue
        if figure > 0:
            figure_color = 255, 255, 255
        else:
            figure_color = 100, 100, 100
        r = elem_size // 2 - 10

        pygame.draw.circle(screen, figure_color, (position[0] + elem_size // 2, position[1] + elem_size // 2), r)
        if abs(figure) == 2:
            r = 5
            negative_color = [255 - e for e in figure_color]
            pygame.draw.circle(screen, negative_color, (position[0] + elem_size // 2, position[1] + elem_size // 2), r)
    

def game_loop(screen: Surface, board: BoardState, ai: AI):
    grid_size = screen.get_size()[0] // 8
    GreenPlates = []
    current_piece = None # a piece that player already mooved (if it exist)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_click_position = event.pos 
                old_x, old_y = [p // grid_size for p in mouse_click_position]

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                new_x, new_y = [p // grid_size for p in event.pos]
                old_x, old_y = [p // grid_size for p in mouse_click_position]
                
                new_board = None
                new_board = board.do_move(old_x, old_y, new_x, new_y, current_piece)
                    
                if new_board is not None:
                    board = new_board
                    current_piece = [new_x, new_y]
                GreenPlates = []
 
            if event.type == pygame.MOUSEBUTTONUP and event.button == 3:
                x, y = [p // grid_size for p in event.pos]
                board.board[y, x] = (board.board[y, x] + 1 + 2) % 5 - 2  # change figure

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    board = board.inverted()

                if event.key == pygame.K_SPACE:
                    if current_piece != None and (len(board.get_possible_moves(current_piece[1], current_piece[0], True)) == 0 or board.max_in_ate_pieces() == 0):
                        current_piece = None
                        board.delete_ate_pieces()
                        
                        board = board.inverted()
                        new_board = ai.next_move(board)
                        if new_board is not None:
                            board = new_board
                        board = board.inverted()
                    else:
                        # todo:
                        # message "you have to do move"
                        ...
        

        draw_board(screen, 0, 0, grid_size, board, GreenPlates)
        if board.is_game_finished:
            font = pygame.font.Font(None, 75)
            if board.get_winner == 1:
                text = font.render("YOU WIN", True, (0, 255, 0))
            else: 
                text = font.render("YOU LOSE", True, (255, 0, 0))
            x, y = map(int, screen.get_size())
            screen.blit(text, [x // 4, y // 2]) 
        
        pygame.display.flip()


pygame.init()

screen: Surface = pygame.display.set_mode([512, 512])
ai = AI(search_depth=2) # full turn depth

game_loop(screen, BoardState.initial_state(), ai)

pygame.quit()

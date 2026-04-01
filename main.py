import pygame as pg
from tiles import Board
#30 x 16 grid

ROW_NUMBER = 16
COL_NUMBER = 30
TILE_SIZE = 30

pg.init()

def main() -> None:
    screen = pg.display.set_mode((1000,600))
    board = Board(ROW_NUMBER,COL_NUMBER,TILE_SIZE)
    board.populate_board()
    board_surface = board.draw_board()

    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
        
        screen.blit(board_surface,(0,0))
        pg.display.update()

if __name__ == '__main__':
    main()
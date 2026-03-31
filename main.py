import pygame as pg
from tiles import Board
#30 x 16 grid

GRID_ROWS = 30
GRID_COLS = 16
TILE_SIZE = 30

pg.init()

def main() -> None:
    screen = pg.display.set_mode((1000,600))
    board = Board((GRID_ROWS,GRID_COLS))
    board.populate_board()
    board_surface = board.draw_board((GRID_ROWS*TILE_SIZE,GRID_COLS*TILE_SIZE))
    print(board_surface.get_size(),screen.get_size())

    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
        
        screen.blit(board_surface,(0,0))
        pg.display.update()

if __name__ == '__main__':
    main()
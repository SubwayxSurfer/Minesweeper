import pygame as pg
from tiles import Board
#30 x 16 grid

pg.init()

def main() -> None:
    screen = pg.display.set_mode((1000,600))
    board = Board((30,16))
    board.populate_board()
    board_surface = board.draw_board((900,480))
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
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
    board.draw_board()

    tile = None


    left_down = False
    running = True
    while running:
        left, _, _ = pg.mouse.get_pressed()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        previous_tile = tile

        if left:
            left_down = True
            mouse_pos = pg.mouse.get_pos()
            tile_pos = board.mouse_to_board(mouse_pos)
            if tile_pos:
                tile = board.get_tile(tile_pos)
                if tile != previous_tile:
                    board.hover_tile(tile)
                    if previous_tile:
                        board.unhover_tile(previous_tile)
            elif previous_tile:
                board.unhover_tile(previous_tile)


        elif left_down:
            left_down = False
            mouse_pos = pg.mouse.get_pos()
            tile_pos = board.mouse_to_board(mouse_pos)
            if tile_pos:
                tile = board.get_tile(tile_pos)
                board.display_tile(tile)
        
        board.draw_frame()
        screen.blit(board.get_board_surface(),(0,0))
        pg.display.update()

if __name__ == '__main__':
    main()
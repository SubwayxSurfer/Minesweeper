import pygame as pg
from tiles import Board
#30 x 16 grid

ROW_NUMBER = 16
COL_NUMBER = 30
TILE_SIZE = 30
MINE_COUNT = 99
BORDER_WIDTH = 5

pg.init()

def game_loop(screen:pg.Surface, board:Board) -> bool:
    board.draw_board()

    tile_pos = (0, 0)

    left_down = False
    right_down = False
    
    running = True
    while running:
        left, _, right = pg.mouse.get_pressed()
        keys = pg.key.get_pressed()
        
        left = left or keys[pg.K_q]
        right = right or keys[pg.K_w]
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    return True
                elif event.key == pg.K_ESCAPE:
                    return False
                
        if board.game_end:
            continue
        
        mouse_pos = pg.mouse.get_pos()
        mouse_verified = board.verify_mouse(mouse_pos)
        if mouse_verified:
            tile_pos = board.mouse_to_board(mouse_pos)

        if right and not right_down:
            right_down = True
            if mouse_verified:
                tile = board.get_tile(tile_pos)
                board.flag_tile(tile)
                
        elif not right:
            right_down = False

        if left:
            left_down = True
            if mouse_verified:
                tile = board.get_tile(tile_pos)
                if tile.is_displayed():
                    if tile.is_number():
                        board.adj_hover(tile)
                else:
                    board.single_hover(tile)

        elif left_down:
            left_down = False
            if mouse_verified:
                board.clear_hover()
                tile = board.get_tile(tile_pos)
                if tile.is_number() and tile.is_displayed():
                    board.display_adj_tiles_number(tile)
                board.display_tile(tile)
            
        
        board.draw_frame()
        screen.blit(board.get_board_surface(),(BORDER_WIDTH,BORDER_WIDTH))
        pg.display.update()
        
    return True
    
def main() -> None:
    screen_dimensions = (COL_NUMBER*TILE_SIZE + 2*BORDER_WIDTH,ROW_NUMBER*TILE_SIZE + 2*BORDER_WIDTH)
    screen = pg.display.set_mode(screen_dimensions)
    screen.fill("#464e56")
    
    pg.draw.polygon(screen,"#34414e",[(0,0),(BORDER_WIDTH,BORDER_WIDTH),(BORDER_WIDTH,screen_dimensions[1]-BORDER_WIDTH),(0,screen_dimensions[1])])
    pg.draw.polygon(screen,"#34414e",[(0,0),(BORDER_WIDTH,BORDER_WIDTH),(screen_dimensions[0]-BORDER_WIDTH,BORDER_WIDTH),(screen_dimensions[0],0)])
    pg.draw.polygon(screen,"#57585A",[(screen_dimensions[0],0),(screen_dimensions[0]-BORDER_WIDTH,BORDER_WIDTH),(screen_dimensions[0]-BORDER_WIDTH,screen_dimensions[1]-BORDER_WIDTH),(screen_dimensions[0],screen_dimensions[1])])
    pg.draw.polygon(screen,"#57585A",[(0,screen_dimensions[1]),(BORDER_WIDTH,screen_dimensions[1]-BORDER_WIDTH),(screen_dimensions[0]-BORDER_WIDTH,screen_dimensions[1]-BORDER_WIDTH),(screen_dimensions[0],screen_dimensions[1])])
    
    
    board = Board(BORDER_WIDTH, ROW_NUMBER,COL_NUMBER,TILE_SIZE,MINE_COUNT)
    
    run = True
    while run:
        run = game_loop(screen, board)
        board.refresh_board()
    

if __name__ == '__main__':
    main()
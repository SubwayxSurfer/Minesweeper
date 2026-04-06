import pygame as pg

class Tile:
    def __init__(self, row:int, column:int, tile_size:int) -> None:
        self.row:int = row
        self.col:int = column
        self.tile_rect:pg.Rect = pg.Rect(column*tile_size,row*tile_size,tile_size,tile_size)

        self.base_state:str = "unknown"
        self.displayed_state:str = self.base_state
        self.true_state:str = "1"

        self.confirmed:bool = False
        self.flagged:bool = False

    def get_tile_rect(self) -> pg.Rect:
        return self.tile_rect
    
    def hover(self) -> None:
        if not self.flagged:
            self.set_display_state("empty")
    
    def unhover(self) -> None:
        if not self.flagged:
            self.set_display_state(self.base_state)
    
    def flag(self) -> None:
        if self.flagged:
            self.set_display_state(self.base_state)
        else:
            self.set_display_state("flag")
        self.flagged = not self.flagged
    
    def set_display_state(self, new_state:str) -> None:
        if not self.confirmed:
            self.displayed_state = new_state

    def get_display_state(self) -> str:
        return self.displayed_state
    
    def display_true_state(self) -> None:
        self.displayed_state = self.true_state
        self.confirmed = True


class Board:
    def __init__(self, row_size:int, col_size:int, tile_size:int) -> None:
        self.tile_list:list[list[Tile]] = []

        self.row_size:int = row_size
        self.col_size:int = col_size
        self.tile_size:int = tile_size
        self.board_size:tuple[int,int] = (col_size*tile_size,row_size*tile_size)
        self.board_surface:pg.Surface = pg.Surface(self.board_size)

        self.tile_img_dict:dict[str,pg.Surface] = {
            "1" : pg.Surface.convert_alpha(pg.image.load("assets/Tile1.png")),
            "2" : pg.Surface.convert_alpha(pg.image.load("assets/Tile2.png")),
            "3" : pg.Surface.convert_alpha(pg.image.load("assets/Tile3.png")),
            "4" : pg.Surface.convert_alpha(pg.image.load("assets/Tile4.png")),
            "5" : pg.Surface.convert_alpha(pg.image.load("assets/Tile5.png")),
            "6" : pg.Surface.convert_alpha(pg.image.load("assets/Tile6.png")),
            "7" : pg.Surface.convert_alpha(pg.image.load("assets/Tile7.png")),
            "8" : pg.Surface.convert_alpha(pg.image.load("assets/Tile8.png")),
            "empty" : pg.Surface.convert_alpha(pg.image.load("assets/TileEmpty.png")),
            "exploded" : pg.Surface.convert_alpha(pg.image.load("assets/TileExploded.png")),
            "flag" : pg.Surface.convert_alpha(pg.image.load("assets/TileFlag.png")),
            "mine" : pg.Surface.convert_alpha(pg.image.load("assets/TileMine.png")),
            "unknown" : pg.Surface.convert_alpha(pg.image.load("assets/TileUnknown.png")),
        }
        self.tile_img_dict = {key : pg.transform.scale(value,(tile_size,tile_size)) for key, value in self.tile_img_dict.items()}
        self.draw_queue:set[Tile] = set()
        
        self.displayed_count:int = 0
        self.mine_count = 99

    def populate_board(self) -> None:
        for row in range(self.row_size):
            self.tile_list.append([])
            for column in range(self.col_size):
                tile = Tile(row, column, self.tile_size)
                self.tile_list[row].append(tile)

    def mouse_to_board(self, mouse_pos:tuple[int,int]) -> tuple[int,int] | None:
        mouse_x, mouse_y = mouse_pos
        board_x, board_y = self.board_size

        #if board is top left
        if not (0 <= mouse_x < board_x and 0 <= mouse_y < board_y):
            return None

        mouse_row = mouse_y // self.tile_size
        mouse_col = mouse_x // self.tile_size

        return (mouse_row,mouse_col)
    
    def get_tile(self, tile_pos:tuple[int,int]) -> Tile:
        row,col = tile_pos
        tile = self.tile_list[row][col]
        return tile

    def hover_tile(self, tile:Tile) -> None:
        tile.hover()
        self.append_draw(tile)

    def unhover_tile(self, tile:Tile) -> None:
        tile.unhover()
        self.append_draw(tile)

    def display_tile(self, tile:Tile) -> None:
        self.append_draw(tile)
        tile.display_true_state()
    
    def append_draw(self, tile:Tile) -> None:
        self.draw_queue.add(tile)
    
    def draw_frame(self):
        if self.draw_queue:
            for tile in self.draw_queue:
                self.draw_tile(tile)
            self.draw_queue.clear()

    def draw_tile(self,tile:Tile):
        tile_rect = tile.get_tile_rect()
        tile_state = tile.get_display_state()
        self.board_surface.blit(self.tile_img_dict[tile_state],tile_rect.topleft)

    def draw_board(self) -> None:
        if not self.tile_list:
            self.populate_board()

        self.board_surface.fill((0,0,0))

        for tile_row in self.tile_list:
            for tile in tile_row:
                self.draw_tile(tile)

    def get_board_surface(self) -> pg.Surface:
        return self.board_surface


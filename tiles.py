import pygame as pg

class Tile:
    def __init__(self, row:int, column:int) -> None:
        self.row = row
        self.col = column

    def scale_pos_to_board(self, tile_size:int) -> pg.Rect:
        tile_rect = pg.Rect(self.col*tile_size,self.row*tile_size,tile_size,tile_size)
        return tile_rect


class Board:
    def __init__(self, row_size:int, col_size:int, tile_size:int) -> None:
        self.tile_list:list[list[Tile]] = []
        self.row_size = row_size
        self.col_size = col_size
        self.tile_size = tile_size

        self.tile_img_dict = {
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

    def populate_board(self) -> None:
        for row in range(self.row_size):
            self.tile_list.append([])
            for column in range(self.col_size):
                tile = Tile(row,column)
                self.tile_list[row].append(tile)

    def draw_board(self) -> pg.Surface:
        if not self.tile_list:
            return "Not populated"
        
        board_surface = pg.Surface((self.col_size*self.tile_size,self.row_size*self.tile_size))

        count = 0
        for tile_row in self.tile_list:
            for tile in tile_row:
                count += 1
                tile_rect = tile.scale_pos_to_board(self.tile_size)
                board_surface.blit(self.tile_img_dict["1"],tile_rect.topleft)


        return board_surface

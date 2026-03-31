import pygame as pg

class Tile:
    def __init__(self, pos:tuple[int]) -> None:
        self.pos = pos

    def get_board_pos(self, tile_size:tuple[int]) -> pg.Rect:
        tile_rect = pg.Rect(self.pos[0]*tile_size[0],self.pos[1]*tile_size[1],*tile_size)

        return tile_rect


class Board:
    def __init__(self, board_size:tuple[int]) -> None:
        self.tile_list = []
        self.board_size = board_size

    def populate_board(self) -> None:
        for row in range(self.board_size[1]):
            self.tile_list.append([])
            for column in range(self.board_size[0]):
                tile = Tile((row,column))
                self.tile_list[row].append(tile)

    def draw_board(self, board_dimensions:tuple[int]) -> pg.Surface:
        if not self.tile_list:
            return "Not populated"
        
        board_surface = pg.Surface(board_dimensions)
        row_size = board_dimensions[0] // self.board_size[0]
        col_size = board_dimensions[1] // self.board_size[1]

        for tile_row in self.tile_list:
            for tile in tile_row:
                tile_rect = tile.get_board_pos((row_size,col_size))
                pg.draw.rect(board_surface,"red",tile_rect,2)

        return board_surface

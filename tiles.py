import pygame as pg
from random import sample, choice

class Tile:
    def __init__(self, row:int, column:int, tile_size:int) -> None:
        self.row:int = row
        self.col:int = column
        self.tile_rect:pg.Rect = pg.Rect(column*tile_size,row*tile_size,tile_size,tile_size)

        self.base_state:str = "unknown"
        self.displayed_state:str = self.base_state
        self.true_state:str = "0"

        self.confirmed:bool = False
        self.flagged:bool = False

    def get_tile_rect(self) -> pg.Rect:
        return self.tile_rect
    
    def get_pos(self) -> tuple[int,int]:
        return (self.row,self.col)
    
    def hover(self) -> None:
        if not self.flagged:
            self.set_display_state("0")
    
    def unhover(self) -> None:
        if not self.flagged:
            self.set_display_state(self.base_state)
    
    def flag(self) -> None:
        if self.flagged:
            self.confirmed = False
            self.set_display_state(self.base_state)
            self.flagged = False
        elif not self.confirmed:
            self.set_display_state("flag")
            self.confirmed = True
            self.flagged = True
    
    def set_true_state(self, true_state:str) -> None:
        self.true_state = true_state
        
    def get_true_state(self) -> str:
        return self.true_state
    
    def set_display_state(self, new_state:str) -> None:
        if not self.confirmed:
            self.displayed_state = new_state

    def get_display_state(self) -> str:
        return self.displayed_state
    
    def display_true_state(self) -> None:
        self.displayed_state = self.true_state
        if self.true_state == "mine":
            self.displayed_state = "exploded"
        self.confirmed = True

    def is_displayed(self) -> bool:
        return True if self.displayed_state == self.true_state else False
    
    def is_confirmed(self) -> bool:
        return True if self.confirmed else False

    def is_flagged(self) -> bool:
        return True if self.flagged else False

    def is_mine(self) -> bool:
        return True if self.true_state == "mine" else False

    def is_empty(self) -> bool:
        return True if self.true_state == "0" else False

    def is_number(self) -> bool:
        return self.true_state.isdigit() and not self.is_empty()

class Board:
    def __init__(self, border_radius:int, row_size:int, col_size:int, tile_size:int, mine_count:int) -> None:
        self.tile_list:list[list[Tile]] = []

        self.border_radius = border_radius
        self.row_size:int = row_size
        self.col_size:int = col_size
        self.tile_count = col_size*row_size
        self.tile_size:int = tile_size
        self.mine_count = mine_count
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
            "0" : pg.Surface.convert_alpha(pg.image.load("assets/TileEmpty.png")),
            "exploded" : pg.Surface.convert_alpha(pg.image.load("assets/TileExploded.png")),
            "flag" : pg.Surface.convert_alpha(pg.image.load("assets/TileFlag.png")),
            "mine" : pg.Surface.convert_alpha(pg.image.load("assets/TileMine.png")),
            "unknown" : pg.Surface.convert_alpha(pg.image.load("assets/TileUnknown.png")),
        }
        self.tile_img_dict = {key : pg.transform.scale(value,(tile_size,tile_size)) for key, value in self.tile_img_dict.items()}
        self.draw_queue:set[Tile] = set()
        
        self.displayed_count:int = 0 
        
        self.hovered_tiles:set[Tile] = set()
        
        self.unpopulated = True
        self.game_end = False

    def populate_board(self) -> None:
        self.tile_list.clear()
        for row in range(self.row_size):
            self.tile_list.append([])
            for column in range(self.col_size):
                tile = Tile(row, column, self.tile_size)
                self.tile_list[row].append(tile)

    def populate_mines(self, initial_tile:Tile) -> None:
        general_pos = self.board_to_general(initial_tile.get_pos())
        general_mines = sample(range(self.tile_count), self.mine_count)
        
        if general_pos in general_mines:
            non_mine_set = set(range(self.tile_count)) - set(general_mines)
            mine_pos = choice(list(non_mine_set))
            
            general_mines.remove(general_pos)
            general_mines.append(mine_pos)
        
        board_mines = [self.general_to_board(general_pos) for general_pos in general_mines]
        
        for board_pos in board_mines:
            tile = self.get_tile(board_pos)
            tile.set_true_state("mine")
            
        self.populate_true_states()

    def populate_true_states(self) -> None:
        for row in range(self.row_size):
            for col in range(self.col_size):
                tile = self.get_tile((row,col))
                if tile.get_true_state() == "mine":
                    continue
                adj_tiles = self.get_adj_tiles((row,col))
                adj_mine_count = sum([True for adj_tile in adj_tiles if adj_tile.get_true_state() ==  "mine"])
                true_state_img = str(adj_mine_count)
                tile.set_true_state(true_state_img)
                
    def general_to_board(self, general_pos:int) -> tuple[int,int]:
        return (general_pos//self.col_size, general_pos%self.col_size)
    
    def board_to_general(self, board_pos:tuple[int,int]) -> int:
        return board_pos[0]*self.col_size + board_pos[1]
        
    def mouse_to_board(self, mouse_pos:tuple[int,int]) -> tuple[int,int]:
        mouse_x, mouse_y = mouse_pos[0] - self.border_radius, mouse_pos[1] - self.border_radius

        mouse_row = mouse_y // self.tile_size
        mouse_col = mouse_x // self.tile_size

        return (mouse_row,mouse_col)
    
    def verify_mouse(self, mouse_pos:tuple[int,int]) -> bool:
        mouse_x, mouse_y = mouse_pos
        board_x, board_y = self.board_size

        if self.border_radius <= mouse_x < board_x + self.border_radius and \
        self.border_radius <= mouse_y < board_y + self.border_radius:
            return True
        
        self.clear_hover()
        
        return False
    
    def verify_pos(self, tile_pos:tuple[int,int]) -> bool:
        row, col = tile_pos
        if 0 <= row < self.row_size and 0 <= col < self.col_size:
            return True
        return False

    def get_tile(self, tile_pos:tuple[int,int]) -> Tile:
        row, col = tile_pos
        tile = self.tile_list[row][col]
        return tile

    def get_adj_tiles(self, tile_pos:tuple[int,int]) -> list[Tile]:
        adj_tiles:list[Tile] = []
        
        adj_changes = [-1,0,1]
        for row_change in adj_changes:
            for col_change in adj_changes:
                if row_change == 0 and col_change == 0:
                    continue
                
                adj_pos = (tile_pos[0] + row_change, tile_pos[1] + col_change)
                if self.verify_pos(adj_pos):
                    adj_tiles.append(self.get_tile(adj_pos))
                    
        return adj_tiles

    def clear_hover(self) -> None:
        for tile in self.hovered_tiles:
            self.unhover_tile(tile)
        self.hovered_tiles.clear()

    def hover_tile(self, tile:Tile) -> None:
        if tile not in self.hovered_tiles and not tile.is_confirmed():
            tile.hover()
            self.append_draw(tile)
            self.hovered_tiles.add(tile)
            
    def single_hover(self, tile:Tile) -> None:
        self.hover_tile(tile)
        for prev_tile in self.hovered_tiles - set([tile]):
            self.hovered_tiles.remove(prev_tile)
            self.unhover_tile(prev_tile)
            
    def adj_hover(self, tile:Tile) -> None:
        adj_tiles = self.get_adj_tiles(tile.get_pos())
        for adj_tile in adj_tiles:
            self.hover_tile(adj_tile)
            
        for prev_tile in self.hovered_tiles-set(adj_tiles):
            self.hovered_tiles.remove(prev_tile)
            self.unhover_tile(prev_tile)
            
    def unhover_tile(self, tile:Tile) -> None:
        tile.unhover()
        self.append_draw(tile)

    def flag_tile(self, tile:Tile) -> None:
        tile.flag()
        self.append_draw(tile)

    def display_tile(self, tile:Tile) -> None:
        if not tile.is_confirmed():
            if self.unpopulated:
                self.populate_mines(tile)
                self.unpopulated = False
            
            tile.display_true_state()
            self.previous_tile = None
            
            true_state = tile.get_true_state()
            if true_state == "0":
                self.display_adj_tiles_empty(tile)
            elif true_state == "mine":
                self.game_end = True
                
            self.append_draw(tile)
    
    def display_adj_tiles_empty(self, starting_tile:Tile) -> None:
        adj_tiles = self.get_adj_tiles(starting_tile.get_pos())
        for tile in adj_tiles:
            self.display_tile(tile)
    
    def display_adj_tiles_number(self, starting_tile:Tile) -> None:
        adj_tiles = self.get_adj_tiles(starting_tile.get_pos())
        flagged_adj_tiles = list(filter(lambda x: x.is_flagged(),adj_tiles))
        if str(len(flagged_adj_tiles)) == starting_tile.get_true_state():
            for tile in adj_tiles:
                self.display_tile(tile)
    
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
                
    def refresh_board(self) -> None:
        self.__init__(self.border_radius, self.row_size, self.col_size, self.tile_size, self.mine_count)

    def get_board_surface(self) -> pg.Surface:
        return self.board_surface


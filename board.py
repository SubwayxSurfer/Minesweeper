from random import sample, choice
from enum import Enum
from typing import Iterator, Any
import pygame as pg

pg.init()

def file_write(text:str) -> None:
    with open("temp.txt", "a") as f:
        f.write(text)
    

class TileType(Enum):
    EMPTY = 1
    NUMBER = 2
    MINE = 3

class Tile:
    def __init__(self, row:int, column:int) -> None:
        self.row:int = row
        self.col:int = column

        self.tile_type:TileType = TileType.EMPTY
        self.number = 0

        self.revealed:bool = False
        self.flagged:bool = False
        self.hovered = False
    
    def pos(self) -> tuple[int,int]:
        return (self.row,self.col)
    
    def set_tile(self, tile_type:TileType, number:int = 0) -> None:
        self.tile_type = tile_type
        if tile_type == TileType.NUMBER and number > 0:
            self.number = number
        elif tile_type == TileType.NUMBER and number == 0:
            self.tile_type = TileType.EMPTY
    
    def set_hovered(self, hovered:bool) -> None:
        if not self.flagged and not self.revealed:
            self.hovered = hovered
    
    def toggle_flag(self) -> None:
        if not self.revealed:
            self.flagged = not self.flagged
    
    def reveal(self) -> None:
        if not self.flagged:
            self.revealed = True

    def is_mine(self) -> bool:
        return self.tile_type == TileType.MINE

    def is_empty(self) -> bool:
        return self.tile_type == TileType.EMPTY
    
    def is_number(self) -> bool:
        return self.tile_type == TileType.NUMBER
       
class Board:
    def __init__(self, row_size:int, col_size:int, mine_count:int) -> None:
        self.tile_list:list[list[Tile]] = []

        self.row_size:int = row_size
        self.col_size:int = col_size
        self.tile_count = col_size*row_size
        self.mine_count = mine_count

        self.draw_queue:set[tuple[int,int]] = set()
        
        self.displayed_count:int = 0 
        
        self.hovered_tiles:set[Tile] = set()
        
        self.unpopulated = True
        self.game_end = False

    def populate_board(self) -> None:
        self.tile_list.clear()
        for row in range(self.row_size):
            self.tile_list.append([])
            for column in range(self.col_size):
                tile = Tile(row, column)
                self.tile_list[row].append(tile)
                self.queue_draw(tile)

    def populate_mines(self, initial_tile:Tile) -> None:
        tile_pos = initial_tile.pos()
        general_pos = tile_pos[0]*self.col_size + tile_pos[1]
        general_mines = sample(range(self.tile_count), self.mine_count)
        
        if general_pos in general_mines:
            non_mine_set = set(range(self.tile_count)) - set(general_mines)
            mine_pos = choice(list(non_mine_set))
            
            general_mines.remove(general_pos)
            general_mines.append(mine_pos)
        
        board_mines = [(general_pos//self.col_size, general_pos%self.col_size) for general_pos in general_mines]
            
        self.populate_tile_states(board_mines)

    def populate_tile_states(self,mine_pos:list[tuple[int,int]]) -> None:
        for row in range(self.row_size):
            for col in range(self.col_size):
                tile_pos = (row,col)
                tile = self.tile_at(tile_pos)
                if tile_pos in mine_pos:
                    tile.set_tile(TileType.MINE)
                else:
                    adj_positions = list(self.adjacent_positions((row,col)))
                    adj_mine_count = sum([True for adj_pos in adj_positions if adj_pos in mine_pos])
                    tile.set_tile(TileType.NUMBER,adj_mine_count)
                self.queue_draw(tile)
          
    def tile_at(self, tile_pos:tuple[int,int]) -> Tile:
        row, col = tile_pos
        tile = self.tile_list[row][col]
        return tile
        
    def verify_pos(self, tile_pos:tuple[int,int]) -> bool:
        row, col = tile_pos
        if 0 <= row < self.row_size and 0 <= col < self.col_size:
            return True
        return False
                
    def adjacent_positions(self, tile_pos:tuple[int,int]) -> Iterator[tuple[int,int]]:
        for row_change in [-1,0,1]:
            for col_change in [-1,0,1]:
                if row_change == 0 and col_change == 0:
                    continue
                
                yield (tile_pos[0] + row_change, tile_pos[1] + col_change)

    def adjacent_tiles(self, tile_pos:tuple[int,int]) -> list[Tile]:
        adj_tiles:list[Tile] = []
        
        adj_positions = self.adjacent_positions(tile_pos)
        for adj_pos in adj_positions:
            if self.verify_pos(adj_pos):
                adj_tiles.append(self.tile_at(adj_pos))
                    
        return adj_tiles

    def clear_hover(self) -> None:
        for tile in self.hovered_tiles:
            self.unhover_tile(tile)
        self.hovered_tiles.clear()
    
    def hover_tile(self, tile:Tile) -> None:
        if tile not in self.hovered_tiles and not tile.revealed:
            tile.set_hovered(True)
            self.queue_draw(tile)
            self.hovered_tiles.add(tile)
            
    def hover_single(self, tile:Tile) -> None:
        self.unhover_tiles()
        self.hover_tile(tile)
            
    def hover_adjacent(self, tile:Tile) -> None:
        self.unhover_tiles()
        
        adj_tiles = self.adjacent_tiles(tile.pos())
        for adj_tile in adj_tiles:
            self.hover_tile(adj_tile)
           
    def unhover_tile(self, tile:Tile) -> None:
        tile.set_hovered(False)
        self.queue_draw(tile)
        
    def unhover_tiles(self) -> None:
        for tile in self.hovered_tiles:
            self.unhover_tile(tile)
        self.hovered_tiles.clear()

    def flag_tile(self, tile:Tile) -> None:
        tile.toggle_flag()
        self.queue_draw(tile)

    def reveal_tile(self, tile:Tile) -> None:
        if self.unpopulated:
            self.populate_mines(tile)
            self.unpopulated = False
        
        if not tile.revealed:
            tile.reveal()
            self.queue_draw(tile)
            
            if tile.is_empty():
                self.reveal_adjacent(tile)
            elif tile.is_mine() and not tile.flagged:
                self.game_end = True
    
    def reveal_adjacent(self, tile:Tile) -> None:
        adj_tiles = self.adjacent_tiles(tile.pos())
        
        if tile.is_empty():
            for adj_tile in adj_tiles:
                self.reveal_tile(adj_tile)
                
        elif tile.is_number():
            flagged_adj_tiles = list(filter(lambda x: x.flagged,adj_tiles))
            if len(flagged_adj_tiles) == tile.number:
                    for tile in adj_tiles:
                        self.reveal_tile(tile)
    
    def queue_draw(self, tile:Tile) -> None:
        self.draw_queue.add(tile.pos())
                
    def flush_draw_queue(self) -> set[tuple[int,int]]:
        output = self.draw_queue.copy()
        self.draw_queue.clear()
        return output

    def apply_action(self, action:tuple[str,Any]) -> None:
        kind = action[0]
        tile = self.tile_at(action[1])
        
        if self.game_end:
            return None
        
        if kind == "left_down":
            if tile.revealed:
                if tile.is_number():
                    self.hover_adjacent(tile)
            else:
                self.hover_single(tile)
        
        elif kind == "left_up":
            self.clear_hover()
            if tile.revealed:
                self.reveal_adjacent(tile)
            else:
                self.reveal_tile(tile)
                
        elif kind == "right_up":
            self.flag_tile(tile)
        
    def reset(self) -> None:
        self.tile_list.clear()
        self.unpopulated = True
        
        self.hovered_tiles.clear()
        self.draw_queue.clear()
        
        self.displayed_count:int = 0 
        self.game_end = False

class BoardRenderer:
    def __init__(self, row_number:int, col_number:int, tile_size:int) -> None:
        self.tile_size = tile_size
        self.border_width = 5
        
        board_dimensions = (col_number*tile_size, row_number*tile_size)
        screen_dimensions = tuple(ax + 2*self.border_width for ax in board_dimensions)
        self.screen = pg.display.set_mode(screen_dimensions)
        self.board_surface = pg.Surface(board_dimensions)
        
        self.screen.fill("#FFFFFF")
        pg.draw.polygon(self.screen,"#34414e",[(0,0),(self.border_width,self.border_width),(self.border_width,screen_dimensions[1]-self.border_width),(0,screen_dimensions[1])])
        pg.draw.polygon(self.screen,"#34414e",[(0,0),(self.border_width,self.border_width),(screen_dimensions[0]-self.border_width,self.border_width),(screen_dimensions[0],0)])
        pg.draw.polygon(self.screen,"#57585A",[(screen_dimensions[0],0),(screen_dimensions[0]-self.border_width,self.border_width),(screen_dimensions[0]-self.border_width,screen_dimensions[1]-self.border_width),(screen_dimensions[0],screen_dimensions[1])])
        pg.draw.polygon(self.screen,"#57585A",[(0,screen_dimensions[1]),(self.border_width,screen_dimensions[1]-self.border_width),(screen_dimensions[0]-self.border_width,screen_dimensions[1]-self.border_width),(screen_dimensions[0],screen_dimensions[1])])
        
        self.tile_img_dict:dict[int|str,pg.Surface] = {
            1 : pg.Surface.convert_alpha(pg.image.load("assets/Tile1.png")),
            2 : pg.Surface.convert_alpha(pg.image.load("assets/Tile2.png")),
            3 : pg.Surface.convert_alpha(pg.image.load("assets/Tile3.png")),
            4 : pg.Surface.convert_alpha(pg.image.load("assets/Tile4.png")),
            5 : pg.Surface.convert_alpha(pg.image.load("assets/Tile5.png")),
            6 : pg.Surface.convert_alpha(pg.image.load("assets/Tile6.png")),
            7 : pg.Surface.convert_alpha(pg.image.load("assets/Tile7.png")),
            8 : pg.Surface.convert_alpha(pg.image.load("assets/Tile8.png")),
            "empty" : pg.Surface.convert_alpha(pg.image.load("assets/TileEmpty.png")),
            "exploded" : pg.Surface.convert_alpha(pg.image.load("assets/TileExploded.png")),
            "flag" : pg.Surface.convert_alpha(pg.image.load("assets/TileFlag.png")),
            "mine" : pg.Surface.convert_alpha(pg.image.load("assets/TileMine.png")),
            "unknown" : pg.Surface.convert_alpha(pg.image.load("assets/TileUnknown.png")),
        }
        self.tile_img_dict = {key : pg.transform.scale(value,(self.tile_size,self.tile_size)) for key, value in self.tile_img_dict.items()}
    
    def tile_image(self, tile:Tile) -> pg.Surface:
        if not tile.revealed:
            if tile.flagged:
                return self.tile_img_dict["flag"]
            elif tile.hovered:
                return self.tile_img_dict["empty"]
            return self.tile_img_dict["unknown"]
        else:
            if tile.is_mine():
                return self.tile_img_dict["exploded"]
            elif tile.is_empty():
                return self.tile_img_dict["empty"]
            
            return self.tile_img_dict[tile.number]
        
    def draw_tiles(self, board:Board) -> None:
        tiles_to_draw = board.flush_draw_queue()
    
        if not tiles_to_draw:
            return None
        
        for tile_pos in tiles_to_draw:
            tile = board.tile_at(tile_pos)
            tile_img = self.tile_image(tile)
            self.board_surface.blit(tile_img, (tile_pos[1]*self.tile_size, tile_pos[0]*self.tile_size))
            
        self.screen.blit(self.board_surface, (self.border_width, self.border_width))
        pg.display.update()
        
class InputHandler:
    def __init__(self, tile_size:int, offset:tuple[int,int], board_size:tuple[int,int]) -> None:
        self.offset = offset
        self.tile_size = tile_size
        self.board_size = board_size
        
        self.left_down = False
        
    def get_events(self):
        return pg.event.get()
            
    def interpret(self, event:pg.Event) -> tuple[str,Any]:
        if event.type == pg.QUIT:
            return ("quit", None)
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                return ("space",None)
        
        mouse_pos = pg.mouse.get_pos()
        if self.is_mouse_on_board(mouse_pos):
            tile_pos = self.mouse_to_tile(mouse_pos)
            
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.left_down = True
                    return ("left_down", tile_pos)
                elif event.button == 3:
                    return ("right_down", tile_pos)
                
            elif event.type == pg.MOUSEBUTTONUP:
                if event.button == 1:
                    self.left_down = False
                    return ("left_up", tile_pos)
                elif event.button == 3:
                    return ("right_up", tile_pos)
                
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_q:
                    self.left_down = True
                    return ("left_down", tile_pos)
                elif event.key == pg.K_w:
                    return ("right_down", tile_pos)
                
            elif event.type == pg.KEYUP:
                if event.key == pg.K_q:
                    self.left_down = False
                    return ("left_up", tile_pos)
                elif event.key == pg.K_w:
                    return ("right_up", tile_pos)
            
            elif self.left_down:
                return ("left_down", tile_pos)
                
        return ("nothing", None)
        
    def mouse_to_tile(self, mouse_pos:tuple[int,int]) -> tuple[int,int]:
        mouse_x, mouse_y = mouse_pos[0] - self.offset[0], mouse_pos[1] - self.offset[1]

        mouse_row = mouse_y // self.tile_size
        mouse_col = mouse_x // self.tile_size

        return (mouse_row,mouse_col)
    
    def is_mouse_on_board(self, mouse_pos:tuple[int,int]) -> bool:
        mouse_x, mouse_y = mouse_pos
        board_x, board_y = self.board_size

        if self.offset[0] <= mouse_x < board_x + self.offset[0] and \
        self.offset[1] <= mouse_y < board_y + self.offset[1]:
            return True
        
        return False


from board import Board

board = Board(16,30,99)
board.populate_board()
board.populate_mines(board.tile_at((0,0)))
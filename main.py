from board import Board, BoardRenderer, InputHandler

ROW_NUMBER = 16
COL_NUMBER = 30
TILE_SIZE = 30

def game_loop(board:Board) -> bool:
    renderer = BoardRenderer(ROW_NUMBER, COL_NUMBER, TILE_SIZE)
    handler = InputHandler(TILE_SIZE, (renderer.border_width, renderer.border_width), (COL_NUMBER*TILE_SIZE,ROW_NUMBER*TILE_SIZE))
    
    board.populate_board()
    
    running = True
    while running:
        for event in handler.get_events():
            action = handler.interpret(event)
            if action[0] == "quit":
                return False
            elif action[0] == "space":
                return True
            elif action[0] != "nothing":
                board.apply_action(action)

        renderer.draw_tiles(board)
        
    return True

def main() -> None:
    board = Board(ROW_NUMBER,COL_NUMBER,99)
    
    running = True
    while running:
        running = game_loop(board)
        board.reset()

if __name__ == '__main__':
    main()
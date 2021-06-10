import pyglet
import player
from config import WINDOW_SIZE, TICK_LENGTH
import board

window = None
batch = pyglet.graphics.Batch()
snake = player.Player(batch)
board = board.Board(batch)
move_available = True


def next_game_tick():
    (expected_tile_x, expected_tile_y, snake_tail) = snake.get_snake_info()
    tile_ahead = board.parse_intention(expected_tile_x, expected_tile_y, snake_tail)
    if tile_ahead == "STOP":
        return None
    snake.eval_tile(tile_ahead)

    global move_available
    move_available = True
    return board.get_board(), snake.get_length()


def input_loop():
    while True:
        next_game_tick()
        board.print_board()
        given_action = input("What to do next: ")
        if given_action.strip() == 'A':
            action = pyglet.window.key.A
        elif given_action.strip() == 'D':
            action = pyglet.window.key.D
        else:
            action = 0
        snake.change_direction(action)


def next_tick(action):
    snake.change_direction(action)
    res = next_game_tick()
    board.print_board()
    return res


def main(mode):
    if mode == 0:
        global window
        window = pyglet.window.Window(WINDOW_SIZE, WINDOW_SIZE)

        @window.event
        def on_draw():
            window.clear()
            batch.draw()

        @window.event
        def on_key_press(symbol, modifiers):
            global move_available
            if move_available:
                player.eventHandler.turn(snake, symbol)
                move_available = False

        pyglet.clock.schedule_interval(lambda _: next_game_tick(), TICK_LENGTH)
        pyglet.app.run()
    elif mode == 1:
        input_loop()


if __name__ == '__main__':
    main(0)

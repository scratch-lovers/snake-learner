import pyglet
import player
from config import WINDOW_SIZE, TICK_LENGTH
import board

window = pyglet.window.Window(WINDOW_SIZE, WINDOW_SIZE)
batch = pyglet.graphics.Batch()
snake = player.Player(batch)
board = board.Board(batch)
move_available = True


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


def next_game_tick():
    (expected_tile_x, expected_tile_y) = snake.expected_tile_ahead()
    # print(expected_tile_x, expected_tile_y)
    tile_ahead = board.parse_intention(expected_tile_x, expected_tile_y)
    snake.eval_tile(tile_ahead)
    global move_available
    move_available = True


def main():
    pyglet.clock.schedule_interval(lambda _: next_game_tick(), TICK_LENGTH)
    pyglet.app.run()


if __name__ == '__main__':
    main()

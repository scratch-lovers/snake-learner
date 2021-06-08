import pyglet
import player
from config import WINDOW_SIZE, TICK_LENGTH
import board

window = pyglet.window.Window(WINDOW_SIZE, WINDOW_SIZE)
batch = pyglet.graphics.Batch()
snake = player.Player(batch)
board = board.Board(batch)


@window.event
def on_draw():
    window.clear()
    batch.draw()


@window.event
def on_key_press(symbol, modifiers):
    player.eventHandler.turn(snake, symbol)


def next_game_tick():
    (expected_tile_x, expected_tile_y) = snake.expected_tile_ahead()
    tile_ahead = board.check_tile(expected_tile_x, expected_tile_y)
    snake.check_tile(tile_ahead)


def main():
    pyglet.clock.schedule_interval(lambda _: next_game_tick(), TICK_LENGTH)
    pyglet.app.run()


if __name__ == '__main__':
    main()

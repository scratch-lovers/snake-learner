from enum import Enum
from pyglet.clock import schedule_interval
from pyglet.app import run
from config import TICK_LENGTH
from move import Move
from board import Board
from screen import Screen


class GameMode(Enum):
    PLAYER = 0
    TENSORFLOW = 1


def main(game_mode: GameMode):
    board = Board()
    setup_actions = board.setup_board()
    if game_mode == GameMode.PLAYER:
        screen = Screen()
        for action in setup_actions:
            screen.draw_action(action)

        schedule_interval(lambda _: _player_loop(board, screen), TICK_LENGTH)
        run()
    else:
        _tensorflow_loop()


def _player_loop(board, screen):
    action = board.parse_move(screen.get_player_move())
    screen.set_player_move(Move.FORWARD)
    screen.draw_action(action)
    screen.unlock_move()


def _tensorflow_loop():
    pass


if __name__ == '__main__':
    main(GameMode.PLAYER)


# def input_loop():
#     while True:
#         next_game_tick()
#         board.print_board()
#         given_action = input("What to do next: ")
#         if given_action.strip() == 'A':
#             action = pyglet.window.key.A
#         elif given_action.strip() == 'D':
#             action = pyglet.window.key.D
#         else:
#             action = 0
#         snake.change_direction(action)


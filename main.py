from enum import Enum
from pyglet.clock import schedule_interval
from pyglet.app import run
from config import TICK_LENGTH
from board import Board
from screen import Screen
from playerState import PlayerState
from move import Move
from action import Action


class GameMode(Enum):
    PLAYER = 0
    TENSORFLOW = 1


def main(game_mode: GameMode) -> None:
    board: Board = Board()
    player_state: PlayerState = PlayerState()
    setup_actions: list[Action] = board.setup_board()
    if game_mode == GameMode.PLAYER:
        screen: Screen = Screen(player_state.get_event_handler())
        for action in setup_actions:
            screen.draw_action(action)

        schedule_interval(lambda _: _player_loop(board, screen, player_state), TICK_LENGTH)
        run()
    else:
        tensorflow_loop()


def _player_loop(board: Board, screen: Screen, player_state: PlayerState) -> None:
    action: Action = board.parse_move(player_state.get_player_move())
    player_state.set_player_move(Move.FORWARD)
    screen.draw_action(action)
    screen.unlock_move()


def tensorflow_loop() -> None:
    pass


if __name__ == '__main__':
    main(GameMode.PLAYER)

import copy
import math
import numpy as np
from board import Board
from board_state import BoardState
from direction import Direction
from move import Move
from action import Action
from tile import Tile


class TFBoard(Board):
    __starting_state: BoardState

    def __init__(self) -> None:
        super().__init__()

    def setup_board(self) -> np.ndarray:
        # potencjalnie można stąd wziąć akcje do archiwizacji
        super().setup_board()
        self.__starting_state = BoardState(
            board=copy.deepcopy(self._board),
            snake=copy.deepcopy(self._snake),
            snake_direction=Direction(self._snake_direction.value),
            current_apple=self._current_apple
        )
        observation = np.append(
            self.__translate_board(), [self.__calculate_apple_distance(), len(self._snake)])
        return observation

    def restart_board(self) -> np.ndarray:
        self._board = copy.deepcopy(self.__starting_state.board)
        self._snake = copy.deepcopy(self.__starting_state.snake)
        self._snake_direction = Direction(self.__starting_state.snake_direction.value)
        self._current_apple = self.__starting_state.current_apple
        observation = np.append(
            self.__translate_board(), [self.__calculate_apple_distance(), len(self._snake)])
        return observation

    def __calculate_apple_distance(self) -> int:
        head_y, head_x = self._snake[0]
        apple_y, apple_x = self._current_apple
        return int(math.sqrt((head_y - apple_y) ** 2 + (head_y - head_x) ** 2))

    def __translate_board(self) -> np.ndarray:
        translated_board: list[list[int]] = [[tile.value for tile in _] for _ in self._board]
        snake_y, snake_x = self._snake[0]
        # this will never break anything
        translated_board[snake_y][snake_x] = 4
        return np.array(translated_board).flatten()

    def parse_move(self, move: Move) -> tuple[Action, np.ndarray]:
        # potencjalnie można stąd wziąć akcje do archiwizacji
        action = super().parse_move(move)
        observation = np.append(
            self.__translate_board(), [self.__calculate_apple_distance(), len(self._snake)])
        return action, observation

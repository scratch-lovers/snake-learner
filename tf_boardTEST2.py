import copy
import math
from enum import Enum
import numpy as np
from typing import List, Tuple

from board import Board
from board_state import BoardState
from direction import Direction
from move import Move
from action import Action
from tile import Tile
from collections import deque


class DirectionAll(Enum):
    UP = 0
    UP_LEFT = 1
    LEFT = 2
    DOWN_LEFT = 3
    DOWN = 4
    DOWN_RIGHT = 5
    RIGHT = 6
    UP_RIGHT = 7


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
        return self.__get_observation()

    def restart_board(self) -> np.ndarray:
        self._board = copy.deepcopy(self.__starting_state.board)
        self._snake = copy.deepcopy(self.__starting_state.snake)
        self._snake_direction = Direction(self.__starting_state.snake_direction.value)
        self._current_apple = self.__starting_state.current_apple
        return self.__get_observation()

    def __calculate_apple_distance(self) -> int:
        head_y, head_x = self._snake[0]
        apple_y, apple_x = self._current_apple
        return int(math.sqrt((head_y - apple_y) ** 2 + (head_y - head_x) ** 2))

    def __translate_board(self) -> np.ndarray:
        translated_board: List[List[int]] = [[tile.value for tile in _] for _ in self._board]
        snake_y, snake_x = self._snake[0]
        # this will never break anything
        translated_board[snake_y][snake_x] = 4
        return np.array(translated_board).flatten()

    def parse_move(self, move: Move) -> Tuple[Action, np.ndarray]:
        # potencjalnie można stąd wziąć akcje do archiwizacji
        action = super().parse_move(move)
        return action, self.__get_observation()

    def __get_distance(self, direction: DirectionAll) -> int:
        y_iter = -1 if direction.value in [0, 1, 7] else (1 if direction.value in [3, 4, 5] else 0)
        x_iter = 1 if direction.value in [1, 2, 3] else (-1 if direction.value in [5, 6, 7] else 0)

        current_y, current_x = self._snake
        current_tile: Tile = Tile.EMPTY
        distance: int = 0

        while current_tile not in [Tile.SNAKE, Tile.WALL]:
            current_y += y_iter
            current_x += x_iter
            distance += 1
            current_tile = super()._check_tile(current_y, current_x)
        return distance

    def __get_observation(self):
        direction_values = range(DirectionAll.UP_RIGHT.value + 1)

        distances: List[int] = [self.__get_distance(DirectionAll(direction)) for direction in direction_values]
        distances_queue = deque(distances)
        direction = self._snake_direction
        offset = -2 if direction == Direction.LEFT \
            else (-4 if direction == Direction.DOWN else (-6 if direction == Direction.RIGHT else 0))
        distances_queue.rotate(offset)
        print(direction, distances, offset, distances_queue)

        return np.append(np.array(distances_queue), [self.__calculate_apple_distance(), self._snake_direction.value])

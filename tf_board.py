import copy
import math
from collections import deque

import numpy as np
from typing import List, Tuple
from enum import Enum
from board import Board
from board_state import BoardState
from direction import Direction
from move import Move
from action import Action
from tile import Tile
from config import BOARD_SIZE


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
    __action_history: List[Action]

    def __init__(self) -> None:
        super().__init__()

    def setup_board(self) -> np.ndarray:
        # potencjalnie można stąd wziąć akcje do archiwizacji
        self.__action_history = super().setup_board()
        self.__starting_state = BoardState(
            board=copy.deepcopy(self._board),
            snake=copy.deepcopy(self._snake),
            snake_direction=Direction(self._snake_direction.value),
            current_apple=self._current_apple
        )
        temp_list = self.__where_apple()
        temp_list += self.__where_obstacle()
        temp_list += self.__what_directions()
        observation = np.array(temp_list).astype(np.float16)
        return np.append(observation, self.__get_observation().astype(np.float16))

    def restart_board(self) -> np.ndarray:
        self._board = copy.deepcopy(self.__starting_state.board)
        self._snake = copy.deepcopy(self.__starting_state.snake)
        self._snake_direction = Direction(self.__starting_state.snake_direction.value)
        self._current_apple = self.__starting_state.current_apple
        temp_list = self.__where_apple()
        temp_list += self.__where_obstacle()
        temp_list += self.__what_directions()
        observation = np.array(temp_list).astype(np.float16)
        return np.append(observation, self.__get_observation().astype(np.float16))
        # action history not implemented

    def __return_apple_coords(self) -> Tuple[int, int]:
        apple_y, apple_x = self._current_apple
        return apple_y, apple_x

    def __return_snake_head_coords(self) -> Tuple[int, int]:
        # translated_board: List[List[int]] = [[tile.value for tile in _] for _ in self._board]
        # snake_y, snake_x = self._snake[0]
        # # this will never break anything
        # translated_board[snake_y][snake_x] = 4
        head_y, head_x = self._snake[0]
        return head_y, head_x

    def __where_apple(self) -> List[int]:
        apple_y, apple_x = self._current_apple
        head_y, head_x = self._snake[0]
        above = 1 if apple_y < head_y else 0
        below = 1 if apple_y > head_y else 0
        left_side = 1 if apple_x < head_x else 0
        right_side = 1 if apple_x > head_x else 0
        return [above, right_side, below, left_side]

    # lewy górny róg to 0, 0
    def __where_obstacle(self) -> List[int]:
        head_y, head_x = self._snake[0]
        # init_up_search = head_y
        # init_down_search = head_y
        # init_left_search = head_x
        # init_right_search = head_x
        is_above = 1 if head_y == 0 or self._board[head_y-1][head_x] == Tile.SNAKE else 0
        is_below = 1 if head_y == BOARD_SIZE - 1 or self._board[head_y+1][head_x] == Tile.SNAKE else 0
        is_left = 1 if head_x == 0 or self._board[head_y][head_x-1] == Tile.SNAKE else 0
        is_right = 1 if head_x == BOARD_SIZE - 1 or self._board[head_y][head_x+1] == Tile.SNAKE else 0
        return [is_above, is_right, is_below, is_left]

    def __what_directions(self) -> List[int]:
        up = 1 if self._snake_direction == Direction.UP else 0
        down = 1 if self._snake_direction == Direction.DOWN else 0
        right = 1 if self._snake_direction == Direction.LEFT else 0
        left = 1 if self._snake_direction == Direction.RIGHT else 0
        return [up, right, down, left]

    def __get_distance(self, direction: DirectionAll) -> int:
        y_iter = -1 if direction.value in [0, 1, 7] else (1 if direction.value in [3, 4, 5] else 0)
        x_iter = 1 if direction.value in [1, 2, 3] else (-1 if direction.value in [5, 6, 7] else 0)

        current_y, current_x = self._snake[0]
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

        distances = [self.__get_distance(DirectionAll(direction)) for direction in direction_values]
        # distances_queue = deque(distances)
        # direction = self._snake_direction
        # offset = 2 if direction == Direction.RIGHT \
        #     else (4 if direction == Direction.DOWN else (6 if direction == Direction.LEFT else 0))
        # distances_queue.rotate(offset)
        scale = math.sqrt(BOARD_SIZE ** 2 * 2)
        distances = np.array(distances)
        # distances_scaled = 1 - 2 * distances / scale
        distances_scaled = distances / scale
        return distances_scaled

    def parse_move(self, move: Move) -> Tuple[Action, np.ndarray]:
        # potencjalnie można stąd wziąć akcje do archiwizacji
        action = super().parse_move(move)
        self.__action_history.append(action)
        temp_list = self.__where_apple()
        temp_list += self.__where_obstacle()
        temp_list += self.__what_directions()
        observation = np.array(temp_list).astype(np.float16)
        return action, np.append(observation, self.__get_observation().astype(np.float16))

    def get_history(self) -> List[Action]:
        return self.__action_history

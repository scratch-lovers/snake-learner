import copy
import math
import numpy as np
from typing import List, Tuple

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
        temp_list = self.__where_apple()
        temp_list += self.__where_obstacle()
        temp_list += self.__what_directions()
        observation = np.array(temp_list)
        return observation

    def restart_board(self) -> np.ndarray:
        self._board = copy.deepcopy(self.__starting_state.board)
        self._snake = copy.deepcopy(self.__starting_state.snake)
        self._snake_direction = Direction(self.__starting_state.snake_direction.value)
        self._current_apple = self.__starting_state.current_apple
        temp_list = self.__where_apple()
        temp_list += self.__where_obstacle()
        temp_list += self.__what_directions()
        observation = np.array(temp_list)
        return observation

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
        init_up_search = head_y
        init_down_search = head_y
        init_left_search = head_x
        init_right_search = head_x
        is_above = 1 if head_y == 0 or self._board[head_y-1][head_x] == Tile.SNAKE else 0
        is_below = 1 if head_y == 9 or self._board[head_y+1][head_x] == Tile.SNAKE else 0
        is_left = 1 if head_x == 0 or self._board[head_y][head_x-1] == Tile.SNAKE else 0
        is_right = 1 if head_x == 9 or self._board[head_y][head_x+1] == Tile.SNAKE else 0
        return [is_above, is_right, is_below, is_left]

    def __what_directions(self) -> List[int]:
        up = 1 if self._snake_direction == Direction.UP else 0
        down = 1 if self._snake_direction == Direction.DOWN else 0
        right = 1 if self._snake_direction == Direction.LEFT else 0
        left = 1 if self._snake_direction == Direction.RIGHT else 0
        return [up, right, down, left]

    def parse_move(self, move: Move) -> Tuple[Action, np.ndarray]:
        # potencjalnie można stąd wziąć akcje do archiwizacji
        action = super().parse_move(move)
        temp_list = self.__where_apple()
        temp_list += self.__where_obstacle()
        temp_list += self.__what_directions()
        observation = np.array(temp_list)
        return action, observation

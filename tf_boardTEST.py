import copy
import math
import numpy as np
from typing import List, Tuple

from board import Board
from board_state import BoardState
from direction import Direction
from move import Move
from action import Action


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
        temp_list = []
        temp_list.append(self.__return_snake_head_coords()[0])
        temp_list.append(self.__return_snake_head_coords()[1])
        temp_list.append(self.__return_apple_coords()[0])
        temp_list.append(self.__return_apple_coords()[1])
        temp_list.append(self._snake_direction.value)
        observation = np.array(temp_list)
        return observation

    def restart_board(self) -> np.ndarray:
        self._board = copy.deepcopy(self.__starting_state.board)
        self._snake = copy.deepcopy(self.__starting_state.snake)
        self._snake_direction = Direction(self.__starting_state.snake_direction.value)
        self._current_apple = self.__starting_state.current_apple
        temp_list = []
        temp_list.append(self.__return_snake_head_coords()[0])
        temp_list.append(self.__return_snake_head_coords()[1])
        temp_list.append(self.__return_apple_coords()[0])
        temp_list.append(self.__return_apple_coords()[1])
        temp_list.append(self._snake_direction.value)
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

    def parse_move(self, move: Move) -> Tuple[Action, np.ndarray]:
        # potencjalnie można stąd wziąć akcje do archiwizacji
        action = super().parse_move(move)
        temp_list = []
        temp_list.append(self.__return_snake_head_coords()[0])
        temp_list.append(self.__return_snake_head_coords()[1])
        temp_list.append(self.__return_apple_coords()[0])
        temp_list.append(self.__return_apple_coords()[1])
        temp_list.append(self._snake_direction.value)
        observation = np.array(temp_list)
        return action, observation

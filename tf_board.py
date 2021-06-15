import copy
import math
from board import Board
from board_state import BoardState
from direction import Direction
from move import Move


class TFBoard(Board):
    __starting_state: BoardState

    def __init__(self) -> None:
        super().__init__()
        self.setup_board()

    def setup_board(self) -> None:
        # potencjalnie można stąd wziąć akcje do archiwizacji
        super().setup_board()
        self.__starting_state = BoardState(
            board=copy.deepcopy(self.__board),
            snake=copy.deepcopy(self.__snake),
            snake_direction=Direction(self.__snake_direction.value),
            current_apple=self.__current_apple
        )

    def restart_board(self) -> None:
        self.__board = copy.deepcopy(self.__starting_state.board)
        self.__snake = copy.deepcopy(self.__starting_state.snake)
        self.__snake_direction = Direction(self.__starting_state.snake_direction.value)
        self.__current_apple = self.__starting_state.current_apple

    def calculate_apple_distance(self):
        head_y, head_x = self.__snake[0]
        apple_y, apple_x = self.__current_apple
        return math.sqrt((head_y - apple_y) ** 2 + (head_y - head_x) ** 2)

    def __translate_board(self) -> list[list[int]]:
        translated_board: list[list[int]] = [[tile.value for tile in _] for _ in self.__board]
        snake_y, snake_x = self.__snake[0]
        # this will never break anything
        translated_board[snake_y][snake_x] = 4
        return translated_board

    def parse_move(self, move: Move) -> tuple[list[list[int]], float, int]:
        # potencjalnie można stąd wziąć akcje do archiwizacji
        super().parse_move(move)
        return self.__translate_board(), self.calculate_apple_distance(), len(self.__snake)

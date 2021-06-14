import random
from config import BOARD_SIZE
from tile import Tile
from move import Move
from direction import Direction
from action import ActionQuit, ActionMove, ActionAddMove


class BoardNew:

    __board: list[list[Tile]] = []
    __snake: list[tuple[int, int]]
    __snake_direction: Direction
    __current_apple: tuple[int, int]

    def __init__(self):
        self.__snake = []

    def __generate_board(self):
        self.__board = [
            [Tile.EMPTY for tile in range(BOARD_SIZE)]
            for row in range(BOARD_SIZE)]

    def parse_move(self, move: Move):
        self.__change_direction(move)
        next_head_y, next_head_x = self.__calculate_next_tile()
        next_tile: Tile = self.__check_tile(next_head_y, next_head_x)

        if next_tile == Tile.APPLE:
            self.__update_snake(next_head_y, next_head_x, True)
            old_apple_y, old_apple_x = self.__current_apple
            self.__board[old_apple_y][old_apple_x] = Tile.EMPTY
            self.__current_apple = self.__generate_apple()
            return ActionAddMove(self.__snake[0], (old_apple_y, old_apple_x), self.__current_apple)
        elif next_tile == Tile.EMPTY:
            old_tail = self.__snake[-1]
            self.__update_snake(next_head_y, next_head_x, False)
            return ActionMove(old_tail, self.__snake[0])
        else:
            # WALL or SNAKE
            return ActionQuit()

    def __change_direction(self, move: Move):
        if move == Move.FORWARD:
            pass
        else:
            if move == Move.TURN_LEFT:
                next_move_value: int = (self.__snake_direction.value + 1) % 4
            else:
                next_move_value: int = (self.__snake_direction.value - 1) % 4
            self.__snake_direction = Direction(next_move_value)

    def __calculate_next_tile(self):
        head_y, head_x = self.__snake[0]

        if self.__snake_direction == Direction.UP:
            head_y -= 1
        elif self.__snake_direction == Direction.LEFT:
            head_x += 1
        elif self.__snake_direction == Direction.DOWN:
            head_y += 1
        else:
            head_x -= 1

        return head_y, head_x

    def __check_tile(self, tile_y: int, tile_x: int) -> Tile:
        if tile_y in range(BOARD_SIZE) and tile_x in range(BOARD_SIZE):
            return self.__board[tile_y][tile_x]
        else:
            return Tile.WALL

    def __update_snake(self, next_head_y, next_head_x, ate_apple: bool):
        self.__board[next_head_y][next_head_x] = Tile.SNAKE
        self.__snake.insert(0, (next_head_y, next_head_x))

        if not ate_apple:
            tail_y, tail_x = self.__board[-1]
            self.__board[tail_y][tail_x] = Tile.EMPTY
            self.__snake.pop()

    def __generate_apple(self) -> tuple[int, int]:
        # TODO check if 'snake percentage' is high enough

        # map the board: TILE -> (TILE, y, x)
        board_indexed = [[(self.__board[row][tile], row, tile) for tile in range(BOARD_SIZE)]
                         for row in range(BOARD_SIZE)]
        board_indexed_flattened = [item for sublist in board_indexed for item in sublist]

        apple_candidates = list(filter(lambda tile: tile[0] == Tile.EMPTY, board_indexed_flattened))

        apple_index: int = random.randint(0, len(apple_candidates) - 1)
        apple_coords: tuple[int, int] = apple_candidates[apple_index][1:]

        self.__board[apple_coords[0]][apple_coords[1]] = Tile.APPLE
        return apple_coords

    def print_board(self):
        for row in self.__board[::-1]:
            for elem in row:
                print('_', end=" ") if elem.value == 0 else print(elem.value, end=" ")
            print()
        print()

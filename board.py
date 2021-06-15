import random
from config import BOARD_SIZE, START_Y, START_X
from tile import Tile
from move import Move
from direction import Direction
from action import ActionQuit, ActionMove, ActionAddMove, ActionAdd, Action


class Board:
    __board: list[list[Tile]] = []
    __snake: list[tuple[int, int]]
    __snake_direction: Direction
    __current_apple: tuple[int, int]

    def __init__(self) -> None:
        self.__snake = []
        self.__snake_direction = Direction.LEFT

    def setup_board(self) -> list[Action]:
        self.__generate_board()
        self.__update_snake(START_Y, START_X, remove_tail=False)
        self.__current_apple = self.__generate_apple()
        apple_y, apple_x = self.__current_apple
        return [ActionAdd((START_Y, START_X), Tile.SNAKE), ActionAdd((apple_y, apple_x), Tile.APPLE)]

    def __generate_board(self) -> None:
        self.__board = [
            [Tile.EMPTY for tile in range(BOARD_SIZE)]
            for row in range(BOARD_SIZE)]

    def parse_move(self, move: Move) -> Action:
        self.__change_direction(move)
        next_head_y, next_head_x = self.__calculate_next_tile()
        next_tile: Tile = self.__check_tile(next_head_y, next_head_x)

        if next_tile == Tile.APPLE:
            self.__update_snake(next_head_y, next_head_x, remove_tail=False)
            old_apple_y, old_apple_x = self.__current_apple
            self.__current_apple = self.__generate_apple()
            return ActionAddMove(self.__snake[0], Tile.SNAKE, (old_apple_y, old_apple_x), self.__current_apple)
        elif next_tile == Tile.EMPTY:
            old_tail: tuple[int, int] = self.__snake[-1]
            self.__update_snake(next_head_y, next_head_x, remove_tail=True)
            return ActionMove(old_tail, self.__snake[0])
        else:
            # WALL or SNAKE
            return ActionQuit()

    def __change_direction(self, move: Move) -> None:
        if move == Move.FORWARD:
            pass
        else:
            if move == Move.TURN_LEFT:
                next_move_value: int = (self.__snake_direction.value + 1) % 4
            else:
                next_move_value: int = (self.__snake_direction.value - 1) % 4
            self.__snake_direction = Direction(next_move_value)

    def __calculate_next_tile(self) -> tuple[int, int]:
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

    def __update_snake(self, next_head_y: int, next_head_x: int, remove_tail: bool) -> None:
        self.__board[next_head_y][next_head_x] = Tile.SNAKE
        self.__snake.insert(0, (next_head_y, next_head_x))

        if remove_tail:
            tail_y, tail_x = self.__snake[-1]
            self.__board[tail_y][tail_x] = Tile.EMPTY
            self.__snake.pop()

    def __generate_apple(self) -> tuple[int, int]:
        # TODO check if 'snake percentage' is high enough

        # map the board: TILE -> (TILE, y, x)
        board_indexed: list[list[tuple[Tile, int, int]]] = [
            [(self.__board[row][tile], row, tile)
             for tile in range(BOARD_SIZE)]
            for row in range(BOARD_SIZE)]
        board_indexed_flattened: list[tuple[Tile, int, int]] = [item for sublist in board_indexed for item in sublist]

        apple_candidates: list[tuple[Tile, int, int]] = list(
            filter(lambda tile: tile[0] == Tile.EMPTY, board_indexed_flattened))

        apple_index: int = random.randint(0, len(apple_candidates) - 1)
        apple_coords: tuple[int, int] = apple_candidates[apple_index][1:]

        self.__board[apple_coords[0]][apple_coords[1]] = Tile.APPLE
        return apple_coords

    def print_board(self) -> None:
        for row in self.__board[::-1]:
            for elem in row:
                print('_', end=" ") if elem.value == 0 else print(elem.value, end=" ")
            print()
        print()

import math

import pyglet.shapes

from config import BOARD_SIZE, TILE_SIZE, COLOUR_RED, START_X, START_Y
from tile import Tile
import random


class Board:

    _board = []

    # a board is a 2 dimensional square list of tiles on which the game takes place
    def __init__(self, batch):
        self.__batch_ref = batch
        self.__generate_board()
        self.current_apple = self.__generate_apple()
        self.__head = None

    def __generate_board(self):
        self._board = [[Tile.EMPTY for tile in range(BOARD_SIZE)] for row in range(BOARD_SIZE)]

    def parse_intention(self, tile_x_px, tile_y_px, snake_tail):

        tile_x = self.px_to_tiles(tile_x_px)
        tile_y = self.px_to_tiles(tile_y_px)
        next_tile = self.__check_tile(tile_x, tile_y)

        if next_tile == Tile.APPLE:
            self.update_snake_tiles(snake_tail, (tile_x_px, tile_y_px), True)
            self.__remove_apple()
            self.current_apple = self.__generate_apple()

        elif next_tile == Tile.WALL or next_tile == Tile.SNAKE:
            # game over
            return "STOP"
        self.update_snake_tiles(snake_tail, (tile_x_px, tile_y_px))
        return next_tile

    def __check_tile(self, tile_x, tile_y):
        if tile_x in range(BOARD_SIZE) and tile_y in range(BOARD_SIZE):
            return self._board[tile_y][tile_x]
        else:
            return Tile.WALL

    @staticmethod
    def px_to_tiles(tile_in_px):
        return int(tile_in_px / TILE_SIZE)

    def update_snake_tiles(self, tail, new_snake_head, ate_apple=False):
        if not ate_apple:
            # remove tail
            (tail_x, tail_y) = (self.px_to_tiles(tail[0]), self.px_to_tiles(tail[1]))
            self._board[tail_y][tail_x] = Tile.EMPTY
        # move the head
        (new_head_x, new_head_y) = (self.px_to_tiles(new_snake_head[0]), self.px_to_tiles(new_snake_head[1]))
        self._board[new_head_y][new_head_x] = Tile.SNAKE
        self.__head = (new_head_x, new_head_y)


    def __generate_apple(self):
        # TODO check if 'snake percentage' is high enough

        # map the board: TILE -> (TILE, y, x)
        board_indexed = [[(self._board[row][tile], row, tile) for tile in range(BOARD_SIZE)]
                         for row in range(BOARD_SIZE)]
        board_indexed_flattened = [item for sublist in board_indexed for item in sublist]

        apple_candidates = list(filter(lambda tile: tile[0] == Tile.EMPTY, board_indexed_flattened))

        apple_index = random.randint(0, len(apple_candidates))
        apple_coords = apple_candidates[apple_index]

        self._board[apple_coords[1]][apple_coords[2]] = Tile.APPLE
        return pyglet.shapes.Rectangle(x=int(apple_coords[2] * TILE_SIZE), y=int(apple_coords[1] * TILE_SIZE),
                                       width=TILE_SIZE, height=TILE_SIZE, color=COLOUR_RED, batch=self.__batch_ref)

    def __remove_apple(self):
        current_apple_x = self.px_to_tiles(self.current_apple.x)
        current_apple_y = self.px_to_tiles(self.current_apple.y)
        self._board[current_apple_y][current_apple_x] = Tile.EMPTY
        self.current_apple = None

    def print_board(self):
        for row in self._board[::-1]:
            for elem in row:
                print('_', end=" ") if elem.value == 0 else print(elem.value, end=" ")
            print()
        print()

    def get_board(self):
        board_values = []
        for row in self._board:
            new_row = []
            for elem in row:
                new_row.append(elem.value)
            board_values.append(new_row)
        return board_values

    def distance_from_apple(self):
        (apple_x, apple_y) = (self.px_to_tiles(self.current_apple.x), self.px_to_tiles(self.current_apple.y))
        return math.sqrt(abs(self.__head[0] - apple_x) ** 2 + abs(self.__head[1] - apple_y) ** 2)

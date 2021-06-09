import pyglet.shapes

from config import BOARD_SIZE, TILE_SIZE, COLOUR_RED
from tiles import Tiles
import random


class Board:

    _board = []

    # a board is a 2 dimensional square list of tiles on which the game takes place
    def __init__(self, batch):
        self._snake_size = 1
        self.__batch_ref = batch
        self.__generate_board()
        self.current_apple = self.__generate_apple()

    def __generate_board(self):
        self._board = [[Tiles.EMPTY for tile in range(BOARD_SIZE)] for row in range(BOARD_SIZE)]

    def parse_intention(self, tile_x_px, tile_y_px):
        if not any(Tiles.APPLE in x for x in self._board):
            self.current_apple = self.__generate_apple()
            new_apple_x = self.__convert_px_to_tiles(self.current_apple.x)
            new_apple_y = self.__convert_px_to_tiles(self.current_apple.y)
            self._board[new_apple_y][new_apple_x] = Tiles.APPLE

        tile_x = self.__convert_px_to_tiles(tile_x_px)
        tile_y = self.__convert_px_to_tiles(tile_y_px)

        next_tile = self.__check_tile(tile_x, tile_y)

        if next_tile == Tiles.APPLE:
            current_apple_x = self.__convert_px_to_tiles(self.current_apple.x)
            current_apple_y = self.__convert_px_to_tiles(self.current_apple.y)
            self._board[current_apple_y][current_apple_x] = Tiles.EMPTY
            self.current_apple = None

            # self.current_apple = self.__generate_apple()
            # new_apple_x = self.__convert_px_to_tiles(self.current_apple.x)
            # new_apple_y = self.__convert_px_to_tiles(self.current_apple.y)
            # self._board[new_apple_y][new_apple_x] = Tiles.APPLE
        elif next_tile == Tiles.WALL or next_tile == Tiles.SNAKE:
            exit(0)

        return next_tile

    def __check_tile(self, tile_x, tile_y):
        if tile_x in range(BOARD_SIZE) and tile_y in range(BOARD_SIZE):
            return self._board[tile_y][tile_x]
        else:
            return Tiles.WALL

    @staticmethod
    def __convert_px_to_tiles(tile_in_px):
        return int(tile_in_px / TILE_SIZE)

    def add_snake_tile(self, tile_x_px, tile_y_px):
        tile_y = self.__convert_px_to_tiles(tile_y_px)
        tile_x = self.__convert_px_to_tiles(tile_x_px)
        self._board[tile_y][tile_x] = Tiles.SNAKE
        self._snake_size += 1

    def __generate_apple(self):
        # TODO check if 'snake percentage' is high enough

        # map the board: TILE -> (TILE, y, x)
        board_indexed = [[(self._board[row][tile], row, tile) for tile in range(BOARD_SIZE)]
                         for row in range(BOARD_SIZE)]
        board_indexed_flattened = [item for sublist in board_indexed for item in sublist]

        apple_candidates = list(filter(lambda tile: tile[0] == Tiles.EMPTY, board_indexed_flattened))

        apple_index = random.randint(0, len(apple_candidates))
        apple_coords = apple_candidates[apple_index]

        self._board[apple_coords[1]][apple_coords[2]] = Tiles.APPLE
        return pyglet.shapes.Rectangle(x=int(apple_coords[2] * TILE_SIZE), y=int(apple_coords[1] * TILE_SIZE),
                                   width=TILE_SIZE, height=TILE_SIZE, color=COLOUR_RED, batch=self.__batch_ref)

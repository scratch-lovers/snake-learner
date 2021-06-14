import pyglet
from config import WINDOW_SIZE, TILE_SIZE, COLOUR_BLUE, COLOUR_RED
from action import ActionQuit, ActionMove, ActionAdd, ActionAddMove
from tile import Tile
from move import Move


class Screen:
    __window: pyglet.window.Window
    __batch: pyglet.graphics.Batch
    __move_available: bool
    __entities: list[pyglet.shapes.Rectangle]
    __next_player_move: Move

    def __init__(self):
        self.__window = pyglet.window.Window(WINDOW_SIZE, WINDOW_SIZE)
        self.__batch = pyglet.graphics.Batch()
        self.__entities = []
        self.__move_available = True
        self.__next_player_move = Move.FORWARD

        @self.__window.event
        def on_key_press(symbol: pyglet.window.key, _):
            if self.__move_available:
                if symbol == pyglet.window.key.A or symbol == pyglet.window.key.LEFT:
                    self.__next_player_move = Move.TURN_LEFT
                elif symbol == pyglet.window.key.D or symbol == pyglet.window.key.RIGHT:
                    self.__next_player_move = Move.TURN_RIGHT
                self.__move_available = False

        @self.__window.event
        def on_draw():
            self.__window.clear()
            self.__batch.draw()

    def unlock_move(self):
        self.__move_available = True

    def draw_action(self, action):
        if isinstance(action, ActionQuit):
            self.__window.close()
        elif isinstance(action, ActionMove):
            self.__move_entity(action.move_from, action.move_to)
        elif isinstance(action, ActionAdd):
            self.__add_entity(action.add_to, action.add_what)
        elif isinstance(action, ActionAddMove):
            self.__add_entity(action.add_to, action.add_what)
            self.__move_entity(action.move_from, action.move_to)

    def __add_entity(self, coords: tuple[int, int], tile: Tile):
        px_y, px_x = self.__tile_to_px(coords)
        entity_colour = COLOUR_BLUE
        if tile == tile.APPLE:
            entity_colour = COLOUR_RED

        self.__entities.append(
            pyglet.shapes.Rectangle(y=px_y, x=px_x, width=TILE_SIZE, height=TILE_SIZE,
                                    color=entity_colour, batch=self.__batch))

    def __move_entity(self, curr_coords: tuple[int, int], new_coords: tuple[int, int]):
        curr_y, curr_x = self.__tile_to_px(curr_coords)
        new_y, new_x = self.__tile_to_px(new_coords)

        curr_entity: pyglet.shapes.Rectangle = next(
            entity for entity in self.__entities
            if entity.y == curr_y and entity.x == curr_x)
        assert curr_entity is not None

        curr_entity.y = new_y
        curr_entity.x = new_x

    def get_player_move(self):
        return self.__next_player_move
    
    def set_player_move(self, player_move):
        self.__next_player_move = player_move

    @staticmethod
    def __tile_to_px(tile: tuple[int, int]):
        return tile[0] * TILE_SIZE, tile[1] * TILE_SIZE
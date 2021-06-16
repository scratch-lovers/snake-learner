from collections import deque
from typing import List, Tuple, Deque
import pyglet
from config import WINDOW_SIZE, TILE_SIZE, COLOUR_BLUE, COLOUR_RED, TICK_LENGTH
from action import ActionQuit, ActionMove, ActionAdd, ActionAddMove, Action
from tile import Tile
from move import Move


class Screen:
    __window: pyglet.window.Window
    __batch: pyglet.graphics.Batch
    __entities: List[pyglet.shapes.Rectangle]
    __move_available: bool
    __next_player_move: Move

    def __init__(self, event_handler=None) -> None:
        self.__window = pyglet.window.Window(WINDOW_SIZE, WINDOW_SIZE)
        self.__batch = pyglet.graphics.Batch()
        self.__entities = []
        self.__move_available = True
        self.__event_handler = event_handler

        @self.__window.event
        def on_key_press(symbol: pyglet.window.key, _) -> None:
            if self.__move_available:
                if symbol == pyglet.window.key.A or symbol == pyglet.window.key.LEFT:
                    self.__event_handler.next_player_move(Move.TURN_LEFT)
                elif symbol == pyglet.window.key.D or symbol == pyglet.window.key.RIGHT:
                    self.__event_handler.next_player_move(Move.TURN_RIGHT)
                self.__move_available = False

        @self.__window.event
        def on_draw() -> None:
            self.__window.clear()
            self.__batch.draw()

    def unlock_move(self) -> None:
        self.__move_available = True

    def draw_action(self, action: Action) -> None:
        if isinstance(action, ActionQuit):
            self.__window.close()
        elif isinstance(action, ActionMove):
            self.__move_entity(action.move_from, action.move_to)
        elif isinstance(action, ActionAdd):
            self.__add_entity(action.add_to, action.add_what)
        elif isinstance(action, ActionAddMove):
            self.__add_entity(action.add_to, action.add_what)
            self.__move_entity(action.move_from, action.move_to)

    def __add_entity(self, coords: Tuple[int, int], tile: Tile) -> None:
        px_y, px_x = self.__tile_to_px(coords)
        entity_colour = COLOUR_BLUE
        if tile == tile.APPLE:
            entity_colour = COLOUR_RED
        self.__entities.append(
            pyglet.shapes.Rectangle(y=px_y, x=px_x, width=TILE_SIZE, height=TILE_SIZE,
                                    color=entity_colour, batch=self.__batch))

    def __move_entity(self, curr_coords: Tuple[int, int], new_coords: Tuple[int, int]) -> None:
        curr_y, curr_x = self.__tile_to_px(curr_coords)
        new_y, new_x = self.__tile_to_px(new_coords)

        curr_entity: pyglet.shapes.Rectangle = next(
            entity for entity in self.__entities
            if entity.y == curr_y and entity.x == curr_x)

        curr_entity.y = new_y
        curr_entity.x = new_x

    def replay_actions(self, actions: List[Action]):
        actions: Deque[Action] = deque(actions)

        def replay_action(_actions: Deque[Action]):
            if _actions:
                self.draw_action(_actions.popleft())

        pyglet.clock.schedule_interval(lambda _: replay_action(actions), TICK_LENGTH)
        pyglet.app.run()
        self.__window.close()

    @staticmethod
    def __tile_to_px(tile: Tuple[int, int]) -> Tuple[int, int]:
        return tile[0] * TILE_SIZE, tile[1] * TILE_SIZE

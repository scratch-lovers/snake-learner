from typing import Union
from dataclasses import dataclass
from tile import Tile


@dataclass(frozen=True)
class ActionQuit:
    pass


@dataclass(frozen=True)
class ActionMove:
    move_from: tuple[int, int]
    move_to: tuple[int, int]


@dataclass(frozen=True)
class ActionAdd:
    add_to: tuple[int, int]
    add_what: Tile


@dataclass(frozen=True)
class ActionAddMove:
    add_to: tuple[int, int]
    add_what: Tile
    move_from: tuple[int, int]
    move_to: tuple[int, int]


Action = Union[ActionQuit, ActionMove, ActionAdd, ActionAddMove]

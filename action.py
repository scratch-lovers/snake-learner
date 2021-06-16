from typing import Union, Tuple
from dataclasses import dataclass
from tile import Tile


@dataclass(frozen=True)
class ActionQuit:
    pass


@dataclass(frozen=True)
class ActionMove:
    move_from: Tuple[int, int]
    move_to: Tuple[int, int]


@dataclass(frozen=True)
class ActionAdd:
    add_to: Tuple[int, int]
    add_what: Tile


@dataclass(frozen=True)
class ActionAddMove:
    add_to: Tuple[int, int]
    add_what: Tile
    move_from: Tuple[int, int]
    move_to: Tuple[int, int]


Action = Union[ActionQuit, ActionMove, ActionAdd, ActionAddMove]

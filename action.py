from dataclasses import dataclass


@dataclass(frozen=True)
class ActionQuit:
    pass


@dataclass(frozen=True)
class ActionMove:
    move_from: tuple[int, int]
    move_to: tuple[int, int]


@dataclass(frozen=True)
class ActionAddMove:
    added_to: tuple[int, int]
    move_from: tuple[int, int]
    move_to: tuple[int, int]

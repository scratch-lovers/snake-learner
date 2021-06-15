from dataclasses import dataclass
from tile import Tile
from direction import Direction


@dataclass(frozen=True)
class BoardState:
    board: list[list[Tile]]
    snake: list[tuple[int, int]]
    snake_direction: Direction
    current_apple: tuple[int, int]
from dataclasses import dataclass

from typing import List, Tuple

from tile import Tile
from direction import Direction


@dataclass(frozen=True)
class BoardState:
    board: List[List[Tile]]
    snake: List[Tuple[int, int]]
    snake_direction: Direction
    current_apple: Tuple[int, int]
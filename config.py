# game window config
from typing import Tuple

WINDOW_SIZE: int = 800

# board config
# WINDOW_SIZE must be divisible by BOARD_SIZE
BOARD_SIZE: int = 10
TILE_SIZE: int = WINDOW_SIZE // BOARD_SIZE

# snake config
# -1 because it's an index
START_X: int = BOARD_SIZE // 2 - 1
START_Y: int = BOARD_SIZE // 2 - 1
COLOUR_BLUE: Tuple[int, int, int] = (55, 55, 255)
COLOUR_RED: Tuple[int, int, int] = (214, 9, 9)

# game loop config
TICK_LENGTH: float = 0.1

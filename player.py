import pyglet
from direction import Direction
import playerEvents
from config import START_X, START_Y, TILE_SIZE, COLOUR_BLUE
from tiles import Tiles

# upper-left center
x_position = START_X
y_position = START_Y


eventHandler = playerEvents.PlayerEvents()


class Player:
    def __init__(self, batch):
        self.snake = [pyglet.shapes.Rectangle(x=x_position, y=y_position, width=TILE_SIZE, height=TILE_SIZE,
                                              color=COLOUR_BLUE, batch=batch)]
        self.direction = Direction.LEFT
        self.batch_ref = batch

    @eventHandler.event
    def on_turn(self, key):
        self.change_direction(key)
        print("Does it work?")

    def move(self):
        head_x, head_y = self.snake[0].x, self.snake[0].y

        if self.direction == Direction.LEFT:
            self.snake[0].x -= TILE_SIZE
        elif self.direction == Direction.RIGHT:
            self.snake[0].x += TILE_SIZE
        elif self.direction == Direction.UP:
            self.snake[0].y += TILE_SIZE
        else:
            self.snake[0].y -= TILE_SIZE

        for tile in self.snake[1:]:
            curr_tile_x, curr_tile_y = tile.x, tile.y
            tile.x = head_x
            tile.y = head_y
            head_x, head_y = curr_tile_x, curr_tile_y

    def change_direction(self, key):
        if key == pyglet.window.key.A:
            self.direction = Direction(self.direction.value % Direction.RIGHT.value + 1)
        elif key == pyglet.window.key.D:
            temp = self.direction.value - 1
            temp = Direction.RIGHT.value if temp == 0 else temp
            self.direction = Direction(temp)

    def add_tile(self, x_pos, y_pos):
        if self.direction == Direction.LEFT:
            x_pos -= TILE_SIZE
        elif self.direction == Direction.RIGHT:
            x_pos += TILE_SIZE
        elif self.direction == Direction.UP:
            y_pos += TILE_SIZE
        else:
            y_pos -= TILE_SIZE

        self.snake.insert(0, pyglet.shapes.Rectangle(x=x_pos, y=y_pos, width=TILE_SIZE, height=TILE_SIZE,
                                                     color=COLOUR_BLUE, batch=self.batch_ref))

    def expected_tile_ahead(self):
        x_pos = self.snake[0].x
        y_pos = self.snake[0].y

        if self.direction == Direction.LEFT:
            x_pos -= TILE_SIZE
        elif self.direction == Direction.RIGHT:
            x_pos += TILE_SIZE
        elif self.direction == Direction.UP:
            y_pos += TILE_SIZE
        else:
            y_pos -= TILE_SIZE

        return x_pos, y_pos

    def eval_tile(self, tile):
        if tile == Tiles.EMPTY:
            self.move()
        elif tile == Tiles.APPLE:
            self.add_tile(self.snake[0].x, self.snake[0].y)
        else:
            print("This should never happen")

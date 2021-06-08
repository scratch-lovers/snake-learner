import pyglet
from direction import Direction

START_X = 200
START_Y = 200
BOX_SIZE = 20


class Player:
    def __init__(self, batch):
        self.snake = [pyglet.shapes.Rectangle(x=START_X, y=START_Y, width=BOX_SIZE, height=BOX_SIZE,
                                              color=(55, 55, 255), batch=batch)]
        self.direction = Direction.LEFT

    @staticmethod
    def on_key_press(symbol, modifiers):
        if symbol == pyglet.window.key.A or symbol == 1:
            return lambda x: x.change_direction(Direction.LEFT)

    def move(self):
        for block in self.snake:
            block.x -= 20

    def change_direction(self, direct):
        if direct == Direction.LEFT:
            if self.direction == Direction.LEFT:
                self.direction = Direction.DOWN
            elif self.direction == Direction.DOWN:
                self.direction = Direction.RIGHT
            elif self.direction == Direction.RIGHT:
                self.direction = Direction.UP
            else:
                self.direction = Direction.LEFT
        elif direct == Direction.DOWN:
            print("ok")
        elif direct == Direction.RIGHT:
            print("ok2")
        else:
            print("ok3")

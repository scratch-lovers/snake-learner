import pyglet


def main():
    window = pyglet.window.Window(600, 600)

    batch = pyglet.graphics.Batch()

    rect_x = 200
    rect_y = 200

    square = pyglet.shapes.Rectangle(x=rect_x, y=rect_y, width=20,
                                     height=20, color=(55, 55, 255), batch=batch)

    @window.event
    def on_draw():
        window.clear()
        batch.draw()

    @window.event
    def on_key_press(symbol, modifiers):
        if symbol == pyglet.window.key.A:
            square.x -= 20

    pyglet.app.run()


if __name__ == '__main__':
    main()

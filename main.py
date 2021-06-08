import pyglet
import player

window = pyglet.window.Window(600, 800)
batch = pyglet.graphics.Batch()


@window.event
def on_draw():
    window.clear()
    batch.draw()


def main():
    snake = player.Player(batch)
    window.on_key_press = snake.on_key_press
    pyglet.clock.schedule_interval(lambda x: snake.move(), 0.1)
    pyglet.app.run()


if __name__ == '__main__':
    main()

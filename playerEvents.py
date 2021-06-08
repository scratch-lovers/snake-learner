import pyglet.event


class PlayerEvents(pyglet.event.EventDispatcher):
    def turn(self, snake, key):
        self.dispatch_event('on_turn', snake, key)


PlayerEvents.register_event_type('on_turn')

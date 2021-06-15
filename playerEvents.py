import pyglet.event


class WindowEvents(pyglet.event.EventDispatcher):
    def next_player_move(self, next_move) -> None:
        self.dispatch_event('receive_player_move', next_move)


WindowEvents.register_event_type('receive_player_move')

from playerEvents import WindowEvents
from move import Move


class PlayerState:

    def __init__(self):
        self.__event_handler = WindowEvents()
        self.__next_player_move = Move.FORWARD

        @self.__event_handler.event
        def receive_player_move(next_move):
            self.__next_player_move = next_move

    def get_player_move(self):
        return self.__next_player_move
    
    def get_event_handler(self):
        return self.__event_handler

    def set_player_move(self, new_move):
        self.__next_player_move = new_move

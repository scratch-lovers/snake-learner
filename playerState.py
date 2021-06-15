from playerEvents import WindowEvents
from move import Move


class PlayerState:

    __next_player_move: Move
    __event_handler: WindowEvents

    def __init__(self) -> None:
        self.__event_handler = WindowEvents()
        self.__next_player_move = Move.FORWARD

        @self.__event_handler.event
        def receive_player_move(next_move) -> None:
            self.__next_player_move = next_move

    def get_player_move(self) -> Move:
        return self.__next_player_move
    
    def get_event_handler(self) -> WindowEvents:
        return self.__event_handler

    def set_player_move(self, new_move) -> None:
        self.__next_player_move = new_move

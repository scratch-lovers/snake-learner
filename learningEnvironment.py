import math
import numpy as np
import tf_agents.environments.py_environment as py_environment
from tf_agents.specs import array_spec
from tf_agents.trajectories import time_step
from tf_agents.environments import utils
from config import BOARD_SIZE
from tf_board import TFBoard
from move import Move
from action import ActionQuit, ActionAddMove, ActionMove, Action


class LearningEnvironment(py_environment.PyEnvironment):

    board: TFBoard
    __episode_ended: bool
    __tick: int
    __board_action: Action
    __observation: np.ndarray
    __max_tick: int
    __max_distance: int

    def __init__(self):
        super().__init__()

        no_of_tiles = BOARD_SIZE * BOARD_SIZE

        minima = [0 for _ in range(no_of_tiles)]
        minima.append(0)
        minima.append(1)
        maxima = [4 for _ in range(no_of_tiles)]
        self.__max_distance = int(math.sqrt((BOARD_SIZE - 1) ** 2 * 2))
        maxima.append(self.__max_distance)
        maxima.append(no_of_tiles)

        self._action_spec = array_spec.BoundedArraySpec(shape=(), dtype=np.int32, minimum=0, maximum=2, name='action')
        self._observation_spec = array_spec.BoundedArraySpec(
            shape=(no_of_tiles + 2, ), dtype=np.int32, minimum=minima,
            maximum=maxima, name='observation')

        self.board = TFBoard()
        self.board.setup_board()
        self.__episode_ended = False
        self.__tick = 0
        self.__max_tick = 1000

    def observation_spec(self):
        return self._observation_spec

    def action_spec(self):
        return self._action_spec

    def _step(self, action):
        self.__tick += 1
        if self.__episode_ended:
            return self.reset()

        move: Move
        if action == 0:
            move = Move.TURN_LEFT
        elif action == 1:
            move = Move.TURN_RIGHT
        elif action == 2:
            move = Move.FORWARD
        else:
            raise ValueError('action should be 0, 1 or 2')

        self.__board_action, self.__observation = self.board.parse_move(move)
        if isinstance(self.__board_action, ActionQuit):
            self.__episode_ended = True

        # self.board.print_board()

        if self.__episode_ended or self.__tick == self.__max_tick:
            return time_step.termination(self.__observation, 0)
        else:
            # TODO remove this
            if not isinstance(self.__board_action, ActionMove):
                print(self.__board_action.add_what)
            if isinstance(self.__board_action, ActionAddMove):
                return time_step.transition(self.__observation, reward=1000000, discount=1.0)
            return time_step.transition(
                self.__observation, reward=(self.__max_distance - self.__observation[BOARD_SIZE * BOARD_SIZE]) ** 2, discount=1.0)

    def _reset(self):
        self.__episode_ended = False
        self.__tick = 0
        self.__observation = self.board.restart_board()
        return time_step.restart(self.__observation)

    def get_info(self):
        pass

    def get_state(self):
        pass

    def set_state(self, state):
        pass


if __name__ == "__main__":
    env = LearningEnvironment()
    utils.validate_py_environment(env, episodes=1)

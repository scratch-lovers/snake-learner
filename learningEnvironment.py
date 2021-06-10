import tf_agents.environments.py_environment as py_environment
import numpy as np
from tf_agents.specs import array_spec
from tf_agents.trajectories import time_step
from tf_agents.environments import utils
import main
import pyglet
from config import BOARD_SIZE


class LearningEnvironment(py_environment.PyEnvironment):

    def __init__(self):
        super().__init__()
        self._action_spec = array_spec.BoundedArraySpec(shape=(), dtype=np.int32, minimum=0, maximum=2, name='action')
        self._observation_spec = array_spec.BoundedArraySpec(shape=(BOARD_SIZE, BOARD_SIZE), dtype=np.int32, minimum=0,
                                                             maximum=3, name='observation')

        self._board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=np.int32)
        self._snake_length = 1
        self._episode_ended = False

    def observation_spec(self):
        return self._observation_spec

    def action_spec(self):
        return self._action_spec

    def _step(self, action):

        if self._episode_ended:
            return self.reset()

        if action == 0:
            res = main.next_tick(pyglet.window.key.A)
            if res is None:
                self._episode_ended = True
            else:
                self._board = np.array(res[0], dtype=np.int32)
                self._snake_length = res[1]
        elif action == 1:
            res = main.next_tick(pyglet.window.key.D)
            if res is None:
                self._episode_ended = True
            else:
                self._board = np.array(res[0], dtype=np.int32)
                self._snake_length = res[1]
        elif action == 2:
            res = main.next_tick(0)
            if res is None:
                self._episode_ended = True
            else:
                self._board = np.array(res[0], dtype=np.int32)
                self._snake_length = res[1]
        else:
            raise ValueError('action should be 0, 1 or 2')

        if self._episode_ended:
            reward = self._snake_length
            return time_step.termination(self._board, reward)
        else:
            return time_step.transition(self._board, reward=0.0, discount=1.0)

    def _reset(self):
        self._snake_length = 1
        self._episode_ended = False
        return time_step.restart(self._board)

    def get_info(self):
        pass

    def get_state(self):
        pass

    def set_state(self, state):
        pass


if __name__ == "__main__":
    env = LearningEnvironment()
    utils.validate_py_environment(env, episodes=1)

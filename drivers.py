from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow as tf


from tf_agents.environments import suite_gym
from tf_agents.environments import tf_py_environment
from tf_agents.policies import random_py_policy
from tf_agents.policies import random_tf_policy
import tf_agents.policies
from tf_agents.metrics import py_metrics
from tf_agents.metrics import tf_metrics
from tf_agents.drivers import py_driver
from tf_agents.drivers import dynamic_episode_driver, dynamic_step_driver
from tf_agents.networks import network
from tf_agents.specs import tensor_spec

from learningEnvironment import LearningEnvironment
import time
import numpy

tf.compat.v1.enable_v2_behavior()


def compute_avg_return(environment, policy, num_episodes=10):
    total_return = 0.0
    for _ in range(num_episodes):
        print('episode number:', _)
        time.sleep(2)
        time_step = environment.reset()
        episode_return = 0.0

        while not time_step.is_last():
            action_step = policy.action(time_step)
            time_step = environment.step(action_step.action)
            environment._env.envs[0].board.print_board()
            time.sleep(0.25)
            episode_return += time_step.reward
        total_return += episode_return

    avg_return = total_return / num_episodes
    return avg_return.numpy()[0]


#######
env = LearningEnvironment()
tf_env = tf_py_environment.TFPyEnvironment(env)

input_tensor_spec = tensor_spec.TensorSpec((102,), tf.int32)
time_step_spec = tf_env.time_step_spec()
action_spec = tf_env.action_spec()
num_actions = env.action_spec().maximum - env.action_spec().minimum + 1

class QNetwork(network.Network):
    def __init__(self, input_tensor_spec, action_spec, num_actions, name=None):
        super(QNetwork, self).__init__(
            input_tensor_spec=input_tensor_spec,
            state_spec=(),
            name=name)
        self._sub_layers = [
            tf.keras.layers.Dense(num_actions),
        ]

    def call(self, inputs, step_type=None, network_state=()):
        del step_type
        inputs = tf.cast(inputs, tf.int32)
        for layer in self._sub_layers:
            inputs = layer(inputs)
        return inputs, network_state


q_net = QNetwork(
    input_tensor_spec, action_spec, num_actions
)

# tf_policy = random_tf_policy.RandomTFPolicy(action_spec=tf_env.action_spec(),
#                                             time_step_spec=tf_env.time_step_spec())
tf_policy = tf_agents.policies.q_policy.QPolicy(
    tf_env.time_step_spec(),
    tf_env.action_spec(),
    q_net
)

num_episodes = tf_metrics.NumberOfEpisodes()
env_steps = tf_metrics.EnvironmentSteps()
observers = [num_episodes, env_steps]
driver = dynamic_step_driver.DynamicStepDriver(
    tf_env, tf_policy, observers, num_steps=30000)

# Initial driver.run will reset the environment and initialize the policy.
final_time_step, policy_state = driver.run()

print('final_time_step', final_time_step)
print('Number of Steps: ', env_steps.result().numpy())
print('Number of Episodes: ', num_episodes.result().numpy())


compute_avg_return(tf_env, tf_policy)

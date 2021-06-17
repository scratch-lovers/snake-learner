from __future__ import absolute_import, division, print_function
import tensorflow as tf
from tf_agents.environments import tf_py_environment
from learningEnvironment import LearningEnvironment
from screen import Screen
from tf_agents.utils import common
from tf_agents.agents.dqn import dqn_agent
from tf_agents.environments import suite_gym
from tf_agents.environments import tf_py_environment
from tf_agents.eval import metric_utils
from tf_agents.metrics import tf_metrics
from tf_agents.networks import sequential
from tf_agents.policies import random_tf_policy, PolicySaver
from tf_agents.replay_buffers import tf_uniform_replay_buffer
from tf_agents.trajectories import trajectory
from tf_agents.specs import tensor_spec
import matplotlib.pyplot as plt

batch_size = 500
eval_py_env = LearningEnvironment()
eval_env = tf_py_environment.TFPyEnvironment(eval_py_env)
train_py_env = LearningEnvironment()
train_env = tf_py_environment.TFPyEnvironment(train_py_env)

def record_snake_length(environment, policy):
    time_step = environment.reset()
    while not time_step.is_last():
        action_step = policy.action(time_step)
        time_step = environment.step(action_step.action)
    return len(environment._env.envs[0].board._snake)

learning_rate = 0.00025
train_step_counter = tf.Variable(0)
fc_layer_params = (128, 128, 128)
action_tensor_spec = tensor_spec.from_spec(train_env.action_spec())
num_actions = action_tensor_spec.maximum - action_tensor_spec.minimum + 1
optimizer = tf.keras.optimizers.Adam(learning_rate=learning_rate)

def dense_layer(num_inputs):
    return tf.keras.layers.Dense(
        num_inputs,
        activation=tf.keras.activations.relu,
        kernel_initializer=tf.keras.initializers.VarianceScaling(
            scale=2.0, mode='fan_in', distribution='truncated_normal'))


dense_layers = [dense_layer(num_units) for num_units in fc_layer_params]
q_values_layer = tf.keras.layers.Dense(
    num_actions,
    activation=None,
    kernel_initializer=tf.keras.initializers.RandomUniform(
        minval=-0.03, maxval=0.03),
    bias_initializer=tf.keras.initializers.Constant(-0.2))
q_net = sequential.Sequential(dense_layers + [q_values_layer])
agent = dqn_agent.DqnAgent(
    train_env.time_step_spec(),
    train_env.action_spec(),
    q_network=q_net,
    optimizer=optimizer,
    td_errors_loss_fn=common.element_wise_squared_loss,
    train_step_counter=train_step_counter)
agent.initialize()

policy = agent.policy

steps = []
for x in range(0, 100000, 5000):
    steps.append(x)

average_lengths = []
games_to_play = 5

for step in steps:
    print(step)

    checkpointer = common.Checkpointer(ckpt_dir='testing/' + str(step), policy=policy)

    # pepega
    if step > 15000:
        eval_env._env.envs[0].max_tick = 10000

    # play 5 games for every step
    curr_lengths = []
    for i in range(games_to_play):
        curr_lengths.append(record_snake_length(eval_env, policy))
    # get the avg
    curr_average = sum(curr_lengths) / games_to_play
    average_lengths.append((curr_average, step))

# plot
y_axis = [x[0] for x in average_lengths]
x_axis = [x[1] for x in average_lengths]
plt.plot(x_axis, y_axis)
plt.show()

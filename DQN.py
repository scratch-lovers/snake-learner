from __future__ import absolute_import, division, print_function
import time
import tensorflow as tf
from tf_agents.agents.dqn import dqn_agent
from tf_agents.environments import tf_py_environment
from tf_agents.networks import sequential
from tf_agents.policies import random_tf_policy
from tf_agents.replay_buffers import tf_uniform_replay_buffer
from tf_agents.trajectories import trajectory
from tf_agents.specs import tensor_spec
from tf_agents.utils import common
from learningEnvironment import LearningEnvironment
import numpy

# HYPERPARAMETERS SECTION
from screen import Screen

num_iterations = 100000  # @param {type:"integer"}

initial_collect_steps = 100  # @param {type:"integer"}
collect_steps_per_iteration = 1  # @param {type:"integer"}
replay_buffer_max_length = 100000  # @param {type:"integer"}

batch_size = 500  # @param {type:"integer"}
learning_rate = 0.00025  # @param {type:"number"}
log_interval = 200  # @param {type:"integer"}

num_eval_episodes = 10  # @param {type:"integer"}
eval_interval = 1000  # @param {type:"integer"}

train_py_env = LearningEnvironment()
eval_py_env = LearningEnvironment()

train_env = tf_py_environment.TFPyEnvironment(train_py_env)
eval_env = tf_py_environment.TFPyEnvironment(eval_py_env)

fc_layer_params = (128, 128, 128)
action_tensor_spec = tensor_spec.from_spec(train_env.action_spec())
num_actions = action_tensor_spec.maximum - action_tensor_spec.minimum + 1


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

optimizer = tf.keras.optimizers.Adam(learning_rate=learning_rate)

train_step_counter = tf.Variable(0)


agent = dqn_agent.DqnAgent(
    train_env.time_step_spec(),
    train_env.action_spec(),
    q_network=q_net,
    optimizer=optimizer,
    td_errors_loss_fn=common.element_wise_squared_loss,
    train_step_counter=train_step_counter)

agent.initialize()

random_policy = random_tf_policy.RandomTFPolicy(train_env.time_step_spec(),
                                                train_env.action_spec())
eval_policy = agent.policy
collect_policy = agent.collect_policy


def compute_avg_return(environment, policy, num_episodes=10, xd=False):
    total_return = 0.0
    for _ in range(num_episodes):
        if xd:
            print('episode number:', _)
            time.sleep(2)
        time_step = environment.reset()
        episode_return = 0.0

        # print("\nTESTJD ", policy.info_spec)

        while not time_step.is_last():
            action_step = policy.action(time_step)
            # print("\nHERERERERREE", action_step.action)
            time_step = environment.step(action_step.action)
            if xd:
                environment._env.envs[0].board.print_board()
                time.sleep(0.1)
            episode_return += time_step.reward
        total_return += episode_return

    _avg_return = total_return / num_episodes
    return _avg_return.numpy()[0]


replay_buffer = tf_uniform_replay_buffer.TFUniformReplayBuffer(
    data_spec=agent.collect_data_spec,
    batch_size=train_env.batch_size,
    max_length=replay_buffer_max_length)


def collect_step(environment, policy, buffer):
    time_step = environment.current_time_step()
    action_step = policy.action(time_step)
    next_time_step = environment.step(action_step.action)
    traj = trajectory.from_transition(time_step, action_step, next_time_step)

    # Add trajectory to the replay buffer
    buffer.add_batch(traj)


def collect_data(env, policy, buffer, steps):
    for _ in range(steps):
        collect_step(env, policy, buffer)


collect_data(train_env, random_policy, replay_buffer, initial_collect_steps)

dataset = replay_buffer.as_dataset(
    num_parallel_calls=3,
    sample_batch_size=batch_size,
    num_steps=2).prefetch(3)

iterator = iter(dataset)

# (Optional) Optimize by wrapping some of the code in a graph using TF function.
agent.train = common.function(agent.train)

# Reset the train step
agent.train_step_counter.assign(0)

# Evaluate the agent's policy once before training.
avg_return = compute_avg_return(eval_env, random_policy, num_eval_episodes)
returns = [avg_return]


def record_game(environment, policy):
    time_step = environment.reset()
    while not time_step.is_last():
        action_step = policy.action(time_step)
        time_step = environment.step(action_step.action)
    return environment._env.envs[0].board.get_history()


def draw_game(actions):
    screen = Screen()
    screen.replay_actions(actions)


checkpoints = [100, 200, 1000, 5000, 10000, 25000, 50000, 100000]
for x in range(0, 100000, 5000):
    checkpoints.append(x)
checkpointer = common.Checkpointer(ckpt_dir='testing/' + str(0) + '/', policy=agent.policy)
checkpointer.save(global_step=tf.convert_to_tensor(0))
for _ in range(num_iterations):

    # Collect a few steps using collect_policy and save to the replay buffer.
    collect_data(train_env, agent.collect_policy, replay_buffer, collect_steps_per_iteration)

    # Sample a batch of data from the buffer and update the agent's network.
    experience, unused_info = next(iterator)
    train_loss = agent.train(experience).loss

    step = agent.train_step_counter.numpy()

    if step % log_interval == 0:
        print('step = {0}: loss = {1}'.format(step, train_loss))

    # pepega
    if step > 15000:
        train_env._env.envs[0].max_tick = 10000
        eval_env._env.envs[0].max_tick = 10000

    if step in checkpoints:
        checkpointer = common.Checkpointer(ckpt_dir='testing/' + str(step) + '/', policy=agent.policy)
        checkpointer.save(global_step=step)
        # avg_return = compute_avg_return(train_env, agent.collect_policy, 1, False)
        # print('step = {0}: Average Return = {1}'.format(step, avg_return))
        # returns.append(avg_return)
        draw_game(record_game(eval_env, agent.policy))

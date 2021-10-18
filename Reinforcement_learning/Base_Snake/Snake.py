import numpy as np
import matplotlib.pyplot as plt
import random
import time
import sys
import logging
from RL_Agent import RL_Agent
import gym
import rewards
#import gym_snake  # don't use the registered snake
from gym_snake.envs.snake_env import SnakeEnv

from Agent import Agent

log = logging.getLogger("miniproject_snake")
log.setLevel(logging.INFO)
log.addHandler(logging.StreamHandler())

# actions
UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

agent = RL_Agent("stink slang")

env = SnakeEnv(grid_size=[10, 10], snake_size=3, reward_func=rewards.food_reward)

#agent.train(env, timesteps=1000000)
agent.continue_training(env, 5000000)
#agent.load()
obs = env.reset()  # construct instance of game
done = False
log.info("start game")

while not done:
    obs, reward, done, info = env.step(agent.get_action(obs))  # pass action to step()
    env.render()
    

env.close()
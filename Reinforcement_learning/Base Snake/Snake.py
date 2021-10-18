import numpy as np
import matplotlib.pyplot as plt
import random
import time
import sys
import logging
import gym
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

agent = Agent()

env = SnakeEnv(grid_size=[25, 25], snake_size=10)
obs = env.reset()  # construct instance of game
agent.pass_observation(obs)
done = False
log.info("start game")
while not done:
    obs, reward, done, info = env.step(agent.get_action())  # pass action to step()
    agent.pass_observation(obs)
    env.render()
        
input()
env.close()
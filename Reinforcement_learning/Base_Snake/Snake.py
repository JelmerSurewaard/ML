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

agent = RL_Agent("Death Food Punishment, expo_rate 0.001", 0.001)

env = SnakeEnv(grid_size=[8, 8], snake_size=3, reward_func=rewards.death_food_punishment)

agent.train(env, timesteps=10000000)
#agent.train_existing_model(env, 100000)
#agent.load()
obs = env.reset()  # construct instance of game
done = False
log.info("start game")

while not done:
    obs, reward, done, info = env.step(agent.get_action(obs))  # pass action to step()
    env.render()
    

env.close()
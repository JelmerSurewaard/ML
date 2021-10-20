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

agent = RL_Agent("SB2-Super-Snake1", 0)

env = SnakeEnv(grid_size=[6,6], snake_size=2, reward_func=rewards.food_reward)

#agent.train(env, timesteps=500000)
#agent.train_existing_model(env, 300000)
#agent.train_exist_ppo(env, timesteps=500000)
agent.load()

obs = env.reset()  # construct instance of game
done = False
log.info("start game")

while not done:
    obs, reward, done, info = env.step(agent.get_action(obs))  # pass action to step()
    env.render()
    

env.close()
import numpy as np
import matplotlib.pyplot as plt
import random
import time
import sys
import logging
from RL_Agent import RL_Agent
import gym
import rewards
import asyncio
#import gym_snake  # don't use the registered snake
from gym_snake.envs.snake_env import SnakeEnv

from Agent import Agent


def train_loop(iterations, agent, steps):
    for i in range(iterations):
        agent.train_existing_model(env, steps)
        print("Finished training session ", (i+1))

log = logging.getLogger("miniproject_snake")
log.setLevel(logging.INFO)
log.addHandler(logging.StreamHandler())

# actions
UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

agent = RL_Agent("DQN-Snake25")

env = SnakeEnv(grid_size=[6, 6], snake_size=2, reward_func=rewards.food_reward)

#agent.train(env, 10000)
agent.load()
train_loop(10, agent, 100000)
    


#agent.load()
obs = env.reset()  # construct instance of game
done = False
log.info("start game")

while not done:
    obs, reward, done, info = env.step(agent.get_action(obs))  # pass action to step()
    env.render()
    

env.close()





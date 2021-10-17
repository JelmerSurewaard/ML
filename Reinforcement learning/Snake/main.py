import numpy as np
import matplotlib.pyplot as plt
import random
import time
import sys
import logging
import gym
import rewards
#import gym_snake  # don't use the registered snake
from gym_snake.envs.snake_env import SnakeEnv
from snake import Snake

log = logging.getLogger("miniproject_snake")
log.setLevel(logging.INFO)
log.addHandler(logging.StreamHandler())

# actions
UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

env = SnakeEnv(grid_size=[8, 8], snake_size=3, reward_function=rewards.food_reward)

snake = Snake('test', 'blue')
snake.train(env, 1000)

for i in range(3):
    obs = env.reset()  # construct instance of game
    done = False
    log.info("start game")
    while not done:
        obs, reward, done, info = env.step(snake.get_action(obs))  # pass action to step()
        env.render()
        
env.close()
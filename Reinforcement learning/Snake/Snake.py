import numpy as np
import matplotlib.pyplot as plt
import random
import time
import sys
import logging
import gym
import Rewards
#import gym_snake  # don't use the registered snake
from gym_snake.envs.snake_env import SnakeEnv

from stable_baselines3 import DQN

log = logging.getLogger("miniproject_snake")
log.setLevel(logging.INFO)
log.addHandler(logging.StreamHandler())

# actions
UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

env = SnakeEnv(grid_size=[8, 8], snake_size=3, reward_function=Rewards.food_reward)

training = True
if training:
    model = DQN("MlpPolicy", env, verbose=1, learning_rate=0.005, gamma=0.99, tensorboard_log="tensorboard_logs/RLSnake/")
    model.learn(total_timesteps=1000000)
    model.save("learned_models/RLSnake")
else:
    model = DQN.load("learned_models/RLSnake")


for i in range(3):
    obs = env.reset()  # construct instance of game
    done = False
    log.info("start game")
    while not done:
        action, state = model.predict(obs)
        obs, reward, done, info = env.step(action)  # pass action to step()
        env.render()
        
env.close()
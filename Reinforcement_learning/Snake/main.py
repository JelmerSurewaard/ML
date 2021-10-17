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
from agent import Agent

log = logging.getLogger("miniproject_snake")
log.setLevel(logging.INFO)
log.addHandler(logging.StreamHandler())

# actions
UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

agent1 = Agent('test1', (0, 255, 0), rewards.food_reward)

agents = [agent1]

env = SnakeEnv(agents, grid_size=[10, 10], snake_size=3)

agent1.train(env, 1000)

for i in range(3):
    obs = env.reset()  # construct instance of game
    done = False
    log.info("start game")
    while not done:
        actions = []
        for agent in agents:
            actions.append((agent.id, agent.get_action()))
        
        obs, reward, done, info = env.step(actions)  # pass action to step()
        print(reward)
        env.render()
        
env.close()
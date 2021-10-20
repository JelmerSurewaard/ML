import gym
from gym import spaces
from gym.envs.classic_control import rendering
from numpy.core.fromnumeric import shape
import numpy as np
import matplotlib.pyplot as plt
import rewards

from snake import SnakeGameSP

SCREEN_HEIGHT = 500
SCREEN_WIDTH = 500

class SnakeSPEnv(gym.Env):
    
    def __init__(self, width=5, height=5, snake_size=3, n_foods=1, reward_function=rewards.base_reward):
        # Game info
        self.height = height
        self.width = width
        self.snake_size = snake_size
        self.n_foods = n_foods
        
        self.reward_function = reward_function
        
        self.game = SnakeGameSP(self.width, self.height, self.snake_size, self.n_foods)
        self.done = self.game.done
        
        # Render info
        self.boxsize_height = SCREEN_HEIGHT / height
        self.boxsize_width = SCREEN_WIDTH / width
        self.viewer = None
        
        #RL info
        self.action_space = spaces.Discrete(4)
        self.observation_space = spaces.Box(low=0, high=3, shape=(self.height, self.width), dtype=np.uint8)
        
    def step(self, action):
        self.game.step(action)
        reward = self.reward_function(self.game.game_ticks, self.game.found_food, self.game.won, self.game.death)
        self.done = self.game.done
        return self.game.field, reward, self.done, self.game.get_info()
    
    def reset(self):
        self.game = SnakeGameSP(self.width, self.height, self.snake_size, self.n_foods)
        return self.game.field
    
    def seed(self, x):
        pass
    
    def render(self, mode='human', frame_rate=.2):
        if self.viewer is None:          
            self.viewer = rendering.Viewer(SCREEN_HEIGHT, SCREEN_WIDTH)

        # Add Background
        self.create_background((0,1,0))
        map = self.game.field
        for i in range(len(map)):
            for j in range(len(map[0])):
                rgb = None
                if map[i][j] == 1:
                    rgb = (1,0,0)
                elif map[i][j] == 2:
                    rgb = (0,0,0)
                elif map[i][j] == 3:
                    rgb = (0,0,1)
                
                if rgb is not None:
                    self.create_cube((j,i),rgb)
                    
        if self.viewer is not None:            
            plt.pause(frame_rate)

        return self.viewer.render(return_rgb_array=mode == 'rgb_array')
    
    def create_cube(self,position,rgb):
        top, bot, left, right = self.generate_render_coords(position)
        cube = rendering.FilledPolygon([(left,top),(right,top),(right,bot),(left,bot)])
        # cube = rendering.FilledPolygon([(left,bot),(200,200),(right,top)])
        cube.set_color(rgb[0],rgb[1],rgb[2])
        self.viewer.add_geom(cube)
    
    def create_background(self,rgb):
        background = rendering.FilledPolygon([(0,0),(0,SCREEN_HEIGHT),(SCREEN_WIDTH,SCREEN_HEIGHT),(SCREEN_WIDTH,0)])
        background.set_color(rgb[0],rgb[1],rgb[2])
        self.viewer.add_geom(background)

    def generate_render_coords(self,position):       
        top = SCREEN_HEIGHT - position[1] * self.boxsize_height
        bot = SCREEN_HEIGHT - (position[1] + 1) * self.boxsize_height
        left = position[0] * self.boxsize_width
        right = (position[0] + 1) * self.boxsize_width
        return top, bot, left, right
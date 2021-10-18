import numpy as np
from dijkstra import find_path, get_valid_direction

class Agent:
    
    def __init__(self):
        pass
    
    def pass_observation(self, observation):
        self.observation = observation
             
        self.head_x, self.head_y = self.get_coordinates(3)
        self.target = find_path(self.observation, (self.head_x, self.head_y))
        
    def get_coordinates(self, val):
        y, x = np.where(self.observation == val)
        if y.size == 0 or x.size == 0:
            return 0, 0
        
        return x[0], y[0]
    
    def create_maze(self):
        self.maze = np.copy(self.observation)
        
        for y in range(len(self.maze)):
            for x in range(len(self.maze[y])):
                if self.maze[y][x] != 2:
                    self.maze[y][x] = 0
                else:
                    self.maze[y][x] = 1
    
    def get_action(self):
        return self.target 
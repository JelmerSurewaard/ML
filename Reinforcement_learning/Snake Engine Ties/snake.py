import numpy as np
import random
from collections import deque
from gym.envs.classic_control import rendering

##############################
# Position is a tuple of (y, x)
#
# Field is described as te following:
#   Free space = 0
#   Snake head = 1
#   Snake body = 2
#   Food = 3

ACTION_UP = 0
ACTION_RIGHT = 1
ACTION_DOWN = 2
ACTION_LEFT = 3

class SnakeGameSP:
    
    def __init__(self, width=5, height=5, snake_size=3, n_foods=1):
        # Game info
        self.size = (height, width)
        self.n_snakes = 1
        self.snake_size = snake_size
        self.n_foods = n_foods
        
        self.game_ticks = 0
        self.tail = deque()
        self.foods = []
        
        # Game status
        self.done = False
        self.death = False
        self.won = False
        self.snake_load_ticks = snake_size
        
        self.found_food = False
        
        self.init_snake()
        self.init_foods()
        self.gen_field()
        
    def init_snake(self):
        y = random.randint(0, self.size[0] - 1)
        x = random.randint(0, self.size[1] - 1)
    
        self.head = (y, x)
        
    def init_foods(self):
        assert self.n_foods < (self.size[0] * self.size[1])
        
        for i in range(self.n_foods):
            self.foods.append(self.gen_food_position())
        
    def init_field(self):
        self.field = []
        for y in range(self.size[0]):
            y = []
            for x in range(self.size[1]):
                y.append(0)
            self.field.append(y)  
        
        self.field = np.asarray(self.field)
        
    def gen_food_position(self):
        posibilitys = self.get_possible_food_spaces()
        if len(posibilitys) > 0:
            i = random.randint(0, len(posibilitys) - 1)
        
            return (posibilitys[i][0], posibilitys[i][1])
        else:
            return None
           
    def gen_field(self):
        self.init_field()
        
        # Food
        for pos in self.foods:
            y, x = pos
            self.field[y][x] = 3
            
        # Tail
        for pos in self.tail:
            y, x = pos
            self.field[y][x] = 2
        
        # Head
        if self.head is not None:
            y, x = self.head
            self.field[y][x] = 1
            
    def get_possible_food_spaces(self):
        self.gen_field()
        return np.argwhere(self.field==0)
               
            
    def step(self, action):
        self.found_food = False
        
        self.game_ticks += 1
        
        new_pos = self.translate_position(self.head, action)
        
        if new_pos is None or self.check_pos_is_tail(new_pos):
            #Snake kills itself
            self.done = True
            self.death = True
            self.head = None
            self.tail.clear()
            self.gen_field()
            return
        else:
            self.tail.appendleft(self.head)
            self.head = new_pos
        
        
        if self.check_pos_is_food(new_pos):    
            self.snake_load_ticks += 1
            self.found_food = True
            
            self.foods.remove(new_pos)
            next_food_pos = self.gen_food_position()
            if next_food_pos is not None:
                self.foods.append(next_food_pos)
            pass
            
        if self.snake_load_ticks > 0:
            self.snake_load_ticks -= 1
        else:
            self.tail.pop()
            
        if len(self.get_walkable_positions()) < 1:
            self.done = True
            self.won = True
            
        self.gen_field()

    def translate_position(self, position, action):
        y, x = position
        
        if action == ACTION_UP:
            y = y - 1
            x = x
        elif action == ACTION_RIGHT:
            y = y 
            x = x + 1   
        elif action == ACTION_DOWN:
            y = y + 1
            x = x    
        elif action == ACTION_LEFT:
            y = y
            x = x - 1
        
        if self.check_pos_within_border((y, x)):
            return (y, x)    
        else:
            return None
        
    
    def check_pos_within_border(self, position):
        y, x = position
        # Lower bound
        if y < 0 or x < 0:
            return False
        # Upper bound
        if y >= self.size[0] or x >= self.size[1]:
            return False
        return True
        
    def check_pos_is_tail(self, position):
        if position is None:
            return True
        
        for i, tail_pos in enumerate(self.tail):
            if tail_pos == position:
                if i != len(self.tail) - 1:
                    return True
        return False
    
    def check_pos_is_food(self, position):
        if position is None:
            return False
        
        for food_pos in self.foods:
            if position == food_pos:
                return True
        
        return False
    
    def get_walkable_positions(self):
        self.gen_field()
        # Get all free spaces
        free = np.argwhere(self.field==0) 
        # Get all food spaces
        food = np.argwhere(self.field==3) 
        
        return np.concatenate((free, food))
    
    def get_info(self):
        return {'episode_length': self.game_ticks}
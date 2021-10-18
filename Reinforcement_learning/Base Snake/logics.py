import util
from dijkstra import find_path, get_direction
from datetime import datetime
import math

class Logics:

    def __init__(self):
        pass

    def update(self, game_map, snake_id):
        self.game_map = game_map
        
        self.obstacles = self.read_obstacles()
        self.food = self.read_food()
        
        self.generate_field_matrix()
        
        snake_pos = util.translate_position(self.read_snake_head(snake_id), game_map.width)
        danger_ratio = self.get_danger_ratio(snake_pos)
        #print(danger_ratio)
        
        if danger_ratio > 0.6:
            action = self.get_safest_direction(snake_pos)
            if action is None:
                self.action = self.get_valid_direction(snake_id)
            else:
                self.action = action
            print('Using safest direction')
        else:
            
            step = find_path(self.field_matrix, snake_pos)
            
            if step is None:
                self.action = self.get_valid_direction(snake_id)
            else:
                self.action = step
        
    def read_obstacles(self):
        obstacles = []
        
        for snake in self.game_map.game_map['snakeInfos']:
            obstacles += snake['positions']
        
        obstacles += self.game_map.game_map["obstaclePositions"]
        
        return obstacles
    
    def read_food(self):
        return self.game_map.game_map['foodPositions']
    
    def read_snake_head(self, snake_id):
        snake = self.game_map.get_snake_by_id(snake_id)
        return snake['positions'][0]
    
    def read_snake_size(self, snake_id):
        snake = self.game_map.get_snake_by_id(snake_id)
        return len(snake['positions'])
    
    def get_valid_direction(self, snake_id):
        for dir in util.Direction:
            if self.game_map.can_snake_move_in_direction(snake_id, dir):
                return dir
            
        #if nothing is possible you die lmao xd
        return util.Direction.DOWN
                
    def generate_field_matrix(self):
        field_matrix = []
        for y in range(self.game_map.height):
            row = []
            for x in range(self.game_map.width):
                row.append(0)
            field_matrix.append(row)
            
        for pos in self.obstacles:
            x, y = util.translate_position(pos, self.game_map.width)
            field_matrix[y][x] = 1
            
        for pos in self.food:
            x, y = util.translate_position(pos, self.game_map.width)
            field_matrix[y][x] = 2
            
        self.field_matrix = field_matrix
        
    def get_danger_ratio(self, pos):
        radius = 3
        
        left_bound = pos[0] - radius
        if left_bound < 0:
            left_bound = 0
        
        right_bound = pos[0] + radius
        if right_bound > self.game_map.width - 1:
            right_bound = self.game_map.width - 1
            
        upper_bound = pos[1] - radius
        if upper_bound < 0:
            upper_bound = 0
        
        lower_bound = pos[1] + radius
        if lower_bound > self.game_map.height - 1:
            lower_bound = self.game_map.height - 1
        full_area = (radius * 2 + 1)**2    
        area = (right_bound - left_bound) * (lower_bound - upper_bound)
        
        obstacle_counter = (full_area - area) * 0.66          
        for y in range(lower_bound - upper_bound):
            pos_y = upper_bound + y
            for x in range(right_bound - left_bound):
                pos_x = left_bound + x
                
                if self.field_matrix[pos_y][pos_x] == 1:
                    obstacle_counter += 1
        if obstacle_counter == 0:
            return 0
        return round(obstacle_counter/full_area, 2)
        
    def get_safest_direction(self, pos):
        check_pos = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        lowest_ratio = None
        lowest_pos = None

        for check in check_pos:
            y_pos = pos[1] + check[1]
            x_pos = pos[0] + check[0]
            if y_pos < 0 or y_pos > self.game_map.height - 1 or x_pos < 0 or x_pos > self.game_map.width - 1:
                pass
            else:   
                if self.field_matrix[y_pos][x_pos] == 0:
                    ratio = self.get_danger_ratio((x_pos, y_pos))
                    if lowest_ratio is None:
                        lowest_ratio = ratio
                        lowest_pos = (x_pos, y_pos)
                    elif ratio < lowest_ratio:
                        lowest_ratio = ratio
                        lowest_pos = (x_pos, y_pos)
        
        if lowest_ratio is None:
            return None            
        return get_direction(pos, lowest_pos)
                
                
    def get_action(self):
        #return util.Direction.DOWN
        return self.action

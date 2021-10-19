import numpy as np

OBSTACLE_VAL = -2
APPLE_VAL = -3
HEAD_VAL = -4

def find_path(map, start_pos):
    base_heatmap = gen_heatmap(map, start_pos)
    
    heatmap, apple_pos = fill_heatmap(base_heatmap, start_pos)
    
    direction = None
    
    if apple_pos is not None:
        pos = find_step_apple_to_snake(heatmap, apple_pos)
        if pos is not None:
            direction = get_direction(start_pos, pos)
        else:
            direction = get_direction(start_pos, apple_pos)
            
    if direction is not None:
      return direction
    else:
      valid_dir = get_valid_direction(heatmap, start_pos)
      if valid_dir is not None:
        return valid_dir
      else:
        return 0

def get_direction(snake_pos, next_pos):
    snake_x, snake_y = snake_pos
    next_x, next_y = next_pos
    
    if next_x < snake_x:
        return 3
    if next_x > snake_x:
        return 1
    if next_y < snake_y:
        return 0
    if next_y > snake_y:
        return 2
        

def get_surrounding_available_positions(heatmap, pos):
    check_pos = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    
    positions = []
    found_apple = None
    
    for check in check_pos:
        y_pos = pos[1] + check[1]
        x_pos = pos[0] + check[0]
        
        if y_pos >= 0 and y_pos < len(heatmap) and x_pos >= 0 and x_pos < len(heatmap[0]):
            if heatmap[y_pos][x_pos] == APPLE_VAL:
                found_apple = (x_pos, y_pos)
            if heatmap[y_pos][x_pos] == -1:
                positions.append((x_pos, y_pos))
    
    return positions, found_apple

def print_heatmap(heatmap):
    for y in range(len(heatmap)):
        print()
        val = ''
        for x in range(len(heatmap[y])):
            val += str(heatmap[y][x])
            val += ' '
        print(val)

def gen_heatmap(map, start_pos):
    for y in range(len(map)):
        for x in range(len(map[y])):
          if map[y][x] == 3:
             map[y][x] = HEAD_VAL
          elif map[y][x] == 2:
              map[y][x] = OBSTACLE_VAL
          elif map[y][x] == 1:
              map[y][x] = APPLE_VAL
          else:
              map[y][x] = -1
                
    map[start_pos[1]][start_pos[0]] = 0
    return map

def fill_heatmap(heatmap, start_pos):
    last_updated = []
    to_update = []
    to_update.append(start_pos)
    apple_pos = None
    
    val = 1
    while len(to_update) != 0:
        last_updated = to_update
        to_update = []
        
        for last_pos in last_updated:
            positions, found_apple = get_surrounding_available_positions(heatmap, last_pos)

            if found_apple is not None:
                apple_pos = found_apple
                break

            for position in positions:
                heatmap[position[1]][position[0]] = val

            to_update += positions
        
        if apple_pos is not None:
            break
        
        val += 1
        
    return heatmap, apple_pos

def find_step_apple_to_snake(heatmap, apple_pos):
    
    last_pos = None
    pos = get_surrounding_lowest_position(heatmap, apple_pos)
    
    while pos is not None:
        last_pos = pos
        pos = get_surrounding_lowest_position(heatmap, pos)
    
    return last_pos
    

def get_surrounding_lowest_position(heatmap, pos):
    check_pos = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    
    lowest_val = None
    lowest_pos = (None, None)
    for check in check_pos:
        y_pos = pos[1] + check[1]
        x_pos = pos[0] + check[0]
        
        if y_pos >= 0 and y_pos < len(heatmap) and x_pos >= 0 and x_pos < len(heatmap[0]):
            if isinstance(heatmap[y_pos][x_pos], float):
                if heatmap[y_pos][x_pos] == 0:
                    return None
                
                if heatmap[y_pos][x_pos] > 0:
                    if lowest_val is None:
                       lowest_pos = (x_pos, y_pos)
                       lowest_val = heatmap[y_pos][x_pos]
                       
                    elif heatmap[y_pos][x_pos] < lowest_val:
                        lowest_pos = (x_pos, y_pos)
                        lowest_val = heatmap[y_pos][x_pos]
                        
    return lowest_pos
  
def get_valid_direction(heatmap, pos):
  check_pos = [(1, 0), (-1, 0), (0, 1), (0, -1)]
  
  for check in check_pos:
      y_pos = pos[1] + check[1]
      x_pos = pos[0] + check[0]
      
      if y_pos > 0 and y_pos < len(heatmap) and x_pos > 0 and x_pos < len(heatmap[0]):
        if heatmap[y_pos][x_pos] != OBSTACLE_VAL:
          return get_direction(pos, (x_pos, y_pos))   
          
  return None

def check_if_path_is_safe(base_heatmap, pos, direction, snake_len):
  possibilities = []
  
  check_pos = [(1, 0), (-1, 0), (0, 1), (0, -1)]
  
  for check in check_pos:
      y_pos = pos[1] + check[1]
      x_pos = pos[0] + check[0]
      
      if y_pos > 0 and y_pos < len(base_heatmap) and x_pos > 0 and x_pos < len(base_heatmap[0]):
        heatmap, apple_pos = fill_heatmap(base_heatmap, (x_pos, y_pos))
        temp_direction = get_direction(pos, (y_pos, x_pos))
        max_val = np.max(heatmap)
        possibilities.append((temp_direction, max_val, apple_pos))
  
  for possibility in possibilities:
    temp_direction, max_val, apple_pos = possibility
                  
#event param
#   food taken = 1
#   death = -1
#   nothing = 0
import numpy as np

def test_reward(event):
    return event

def surviving_reward(event, step_amount):
    return (step_amount)

def food_reward(event, step_amount, apple_count, coord):
    
    if event == 1:
        return 250
    if event == -1:
        print("I ate " + str(apple_count) + " apples this game")
        return -1000

    snake_head = np.where(coord == 3)
    fruit_pos = np.where(coord == 1)
    
    if snake_head[0].size != 0:
        pos_x = snake_head[0][0]
        pos_y = snake_head[1][0]
        if fruit_pos[0].size != 0:
            fruit_x = fruit_pos[0][0]
            fruit_y = fruit_pos[1][0]

            dis = abs(fruit_x - pos_x) + abs(fruit_y - pos_y)

            #print("dis: " + str(dis))
            
            #print("result: " + str(result))
            return -dis

    return 0

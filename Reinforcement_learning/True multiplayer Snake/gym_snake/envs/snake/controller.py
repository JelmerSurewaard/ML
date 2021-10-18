from gym_snake.envs import snake
from gym_snake.envs.snake import Snake
from gym_snake.envs.snake import Grid
import numpy as np
import sys
import logging


log = logging.getLogger("miniproject_snake")
log.setLevel(logging.INFO)
log.addHandler(logging.StreamHandler())


class Controller():
    """
    This class combines the Snake, Food, and Grid classes to handle the game logic.
    """

    def __init__(self, agents, grid_size=[30, 30], unit_size=10, unit_gap=1, snake_size=3, n_foods=1, random_init=True):

        self.agents = agents
        n_snakes = len(agents)

        assert n_snakes < grid_size[0]//3
        assert n_snakes < 25
        assert snake_size < grid_size[1]//2
        assert unit_gap >= 0 and unit_gap < unit_size

        self.snakes_remaining = n_snakes
        
        agent_colors = []
        for agent in self.agents:
            agent_colors.append(agent.color)
        
        self.grid = Grid(agent_colors, grid_size, unit_size, unit_gap)
        self.HEAD_COLOR_DIFF = 125

        self.snakes = {}
        self.dead_snakes = []
        
        for i, agent in enumerate(agents):
            start_coord = [(i + 1)*grid_size[0]//(n_snakes + 1), snake_size + 1]
            snake = Snake(agent.color, start_coord, snake_size)
            snake.color = agent.color
            self.snakes[agent.id] = snake
            self.grid.draw_snake(snake, agent.color)
            
        # OLD TURN BASED SNAKE LOGIC
        # for i in range(1, n_snakes+1):
        #     start_coord = [i*grid_size[0]//(n_snakes+1), snake_size+1]
        #     self.snakes.append(Snake(start_coord, snake_size))
        #     color = [self.grid.HEAD_COLOR[0], i *
        #              self.HEAD_COLOR_DIFF-self.HEAD_COLOR_DIFF, 0]
        #     self.snakes[-1].head_color = color
        #     self.grid.draw_snake(self.snakes[-1], color)
        #     self.dead_snakes.append(None)

        if not random_init:
            for i in range(2, n_foods+2):
                start_coord = [i*grid_size[0]//(n_foods+2), grid_size[1]-5]
                self.grid.place_food(start_coord)
        else:
            for i in range(n_foods):
                self.grid.new_food()

    def move_snake(self, direction, snake_id):
        """
        Moves the specified snake according to the game's rules dependent on the direction.
        Does not draw head and does not check for reward scenarios. See move_result for these
        functionalities.
        """

        snake = self.snakes[snake_id]
        if snake is None:
            return None

        # Cover old head position with body
        self.grid.cover(snake.head, snake.color)
        # Erase tail without popping so as to redraw if food eaten
        self.grid.erase(snake.body[0])
        # Find and set next head position conditioned on direction
        return snake.action(direction)

    def move_result(self, snake_id=0):
        """
        Checks for food and death collisions after moving snake. Draws head of snake if
        no death scenarios.
        """

        snake = self.snakes[snake_id]
        if snake is None:
            return 0

        # Check for death of snake
        if self.grid.check_death(snake.head):
            # Avoid miscount of grid.open_space
            self.grid.cover(snake.head, snake.color)
            self.grid.connect(snake.body.popleft(),
                              snake.body[0], self.grid.SPACE_COLOR)
            
            self.kill_snake(snake_id)
            
            reward = -1
            
        # Check for reward
        elif self.grid.food_space(snake.head):
            self.grid.draw(snake.body[0], self.grid.BODY_COLOR)  # Redraw tail
            self.grid.connect(
                snake.body[0], snake.body[1], self.grid.BODY_COLOR)
            # Avoid miscount of grid.open_space
            self.grid.cover(snake.head, snake.color)
            reward = 1
            self.grid.new_food()
            
        else:
            reward = 0
            empty_coord = snake.body.popleft()
            self.grid.connect(
                empty_coord, snake.body[0], self.grid.SPACE_COLOR)
            self.grid.draw(snake.head, snake.color)
            
        if self.snakes[snake_id] is not None:
            self.grid.connect(snake.body[-1], snake.head, snake.color)

        return reward

    def kill_snake(self, snake_id):
        """
        Deletes snake from game and subtracts from the snake_count 
        """

        if self.snakes[snake_id] is None:
            return

        self.grid.erase(self.snakes[snake_id].head)
        self.grid.erase_snake_body(self.snakes[snake_id])
        self.snakes[snake_id] = None
        self.snakes_remaining -= 1

    def step(self, actions):
        """
        Takes an action for each snake in the specified direction and collects their rewards
        and dones.

        directions - tuple, list, or ndarray of directions corresponding to each snake.
        """
        
        if self.snakes_remaining < 1 or self.grid.open_space < 1:
            print('Closes early')
            return self.grid.grid.copy(), [0]*len(actions), True, {"snakes_remaining": self.snakes_remaining}
        
        rewards = {}
    
        if type(actions) is np.int32 or type(actions) is np.int64:
            snake_id = list(self.snakes.keys())[0]
            if self.snakes[snake_id] is None:
                # Snake is dead
                self.kill_snake()
            else:
                # Snake is alive
                next_pos = self.move_snake(actions, snake_id)
                rewards[snake_id] = self.move_result(snake_id)  
        else:
        
            next_positions = {}

            for action in actions:
                snake_id, direction = action

                if self.snakes[snake_id] is None:
                    # Snake is dead
                    self.kill_snake(snake_id)
                else:
                    # Snake is alive
                    next_pos = self.move_snake(direction, snake_id)

                    if next_pos is None:
                        continue
                    
                    for snake_id_temp, pos in next_positions.items():
                        if np.array_equal(next_pos, pos):
                            print('Killing: ', snake_id, ' & ', snake_id_temp)
                            self.kill_snake(snake_id)
                            self.kill_snake(snake_id_temp)

                    next_positions[snake_id] = next_pos

                    rewards[snake_id] = self.move_result(snake_id)                   
        
        done = self.snakes_remaining < 1 or self.grid.open_space < 1
        
        return self.grid.grid.copy(), rewards, done, {"snakes_remaining": self.snakes_remaining}
    
        ############################
        # OLD TURN BASED MULTIPLAYER
        ############################

        # # Ensure no more play until reset
        # if self.snakes_remaining < 1 or self.grid.open_space < 1:
        #     if type(actions) == type(int()) or len(actions) == 1:
        #         return self.grid.grid.copy(), 0, True, {"snakes_remaining": self.snakes_remaining}
        #     else:
        #         return self.grid.grid.copy(), [0]*len(actions), True, {"snakes_remaining": self.snakes_remaining}

        # rewards = []

        
        # # old code: if type(directions) == type(int())
        # # apparently changes from int to np.int64 using Tensorflow and to np.int32 using PyTorch after 1st step?
        # # if type(directions) == type(np.int32()) or type(directions) == type(np.int64()) or type(directions) == type(int()):
        # #     directions = [directions]

        # actions = [actions]
        
        # for i, direction in enumerate(actions):
        #     if self.snakes[i] is None and self.dead_snakes[i] is not None:
        #         self.kill_snake(i)
        #     if direction != -1:  # Erco: -1 is NOMOVE; in that case no movement, and no need to add reward to rewards list
        #         self.move_snake(direction, i)
        #         rewards.append(self.move_result(direction, i))

        # done = self.snakes_remaining < 1 or self.grid.open_space < 1
        # if len(rewards) == 1:
        #     return self.grid.grid.copy(), rewards[0], done, {"snakes_remaining": self.snakes_remaining}
        # else:
        #     return self.grid.grid.copy(), rewards, done, {"snakes_remaining": self.snakes_remaining}

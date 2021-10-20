def base_reward():
    return 0

def simple_reward(game_ticks, found_food, won, death):
    return 10

def death_reward(game_ticks, found_food, won, death):
    if death:
        return -250
    return 10

def food_reward(game_ticks, found_food, won, death):
    if death:
        return -250
    if found_food:
        return 250
    return 10
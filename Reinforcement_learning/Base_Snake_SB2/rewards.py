#event param
#   food taken = 1
#   death = -1
#   nothing = 0

def test_reward(event):
    return event

def surviving_reward(event, step_amount):
    return (step_amount)

def food_reward(event, step_amount, apple_count):
    if event == 1:
        return 1
    if event == -1:
        return -1
    return 0

def food_reward_v2(event, step_amount, apple_count):
    if event == 1:
        return apple_count * 100
    if event == -1:
        return -250
    return 0

def food_reward_v3(event, step_amount, apple_count):
    if event == 1:
        return apple_count * 125
    if event == 0:
        return 1
    if event == -1:
        return -250
    return 0
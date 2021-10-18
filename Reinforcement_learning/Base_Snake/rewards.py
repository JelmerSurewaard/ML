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
        return 50
    if event == 0:
        return -1
    if event == -1:
        return -250
    return 0



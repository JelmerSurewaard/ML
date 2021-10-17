#event param
#   food taken = 1
#   death = -1
#   nothing = 0

def test_reward(event):
    return event

def surviving_reward(event, step_amount):
    return (step_amount * 100)

def food_reward(event, step_amount):
    if event == 1:
        return 50
    return 0
    
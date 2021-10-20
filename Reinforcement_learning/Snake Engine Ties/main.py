from snakeEnv import SnakeSPEnv
from RL_agent import RL_Agent
import rewards


agent = RL_Agent('Stage 2')

env = SnakeSPEnv(width=8, height=8, n_foods=1, snake_size=2, reward_function=rewards.food_reward)


#agent.train(env, 500000, 0.02)
#agent.train_existing_model(env, 500000, 'death reward')
agent.load()

obs = env.reset()
done = False
env.render()


while not done:
    env.render()
    obs, reward, done, info = env.step(agent.get_action(obs))
    
env.close()
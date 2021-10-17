from stable_baselines3 import DQN

class Agent:
    
    def __init__(self, id, color, reward_function):
        self.id = id
        self.color = color
        self.reward_function = reward_function
        
    def train(self, env, timesteps):
        self.model = DQN("MlpPolicy", env, verbose=1, learning_rate=0.005, gamma=0.99, tensorboard_log="tensorboard_logs/RLSnake/" + str(self.id))
        self.model.learn(total_timesteps=timesteps)
        self.model.save("learned_models/RLSnake_" + str(self.id))
        
    def load(self):
        self.model = DQN.load("learned_models/RLSnake_" + str(self.id))
        
    def get_action(self, obs):
        action, state = self.model.predict(obs)
        return (self.id, action)

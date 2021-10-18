import numpy as np
from stable_baselines3 import DQN

class RL_Agent:
    
    def __init__(self, id):
        self.id = id
        
    def train_existing_model(self, env, timesteps):
        custom_objects = {"exploration_initial_eps": 0.05,"exploration_final_eps": 0.05}
        self.model = DQN.load("learned_models/RLSnake_" + str(self.id), env=env, custom_objects=custom_objects)       
        self.model.learn(timesteps)
        self.model.save("learned_models/RLSnake_" + str(self.id))

    def train(self, env, timesteps):
        self.model = DQN("MlpPolicy", env, verbose=1, learning_rate=0.005, gamma=0.99, tensorboard_log="tensorboard_logs/RLSnake/" + str(self.id), exploration_final_eps=0.05)
        self.model.learn(total_timesteps=timesteps)
        self.model.save("learned_models/RLSnake_" + str(self.id))
        
    def load(self):
        self.model = DQN.load("learned_models/RLSnake_" + str(self.id))
        
    def get_action(self, obs):
        action, state = self.model.predict(obs)
        return action


   

  
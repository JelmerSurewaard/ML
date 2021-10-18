import numpy as np
from stable_baselines3 import DQN

class RL_Agent:
    
    def __init__(self, id, final_expo_rate):
        self.id = id
        self.final_expo_rate = final_expo_rate
        
    def train_existing_model(self, env, timesteps):
        custom_objects = {"exploration_initial_eps": self.final_expo_rate,"exploration_final_eps": self.final_expo_rate}
        self.model = DQN.load("learned_models/RLSnake_" + str(self.id), custom_objects=custom_objects)       
        self.model.set_env(env)
        self.model.learn(timesteps)
        self.model.save("learned_models/RLSnake_" + str(self.id))

    def train(self, env, timesteps):
        self.model = DQN("MlpPolicy", env, verbose=1, learning_rate=0.005, gamma=0.99, tensorboard_log="tensorboard_logs/RLSnake/" + str(self.id), exploration_final_eps=self.final_expo_rate)
        self.model.learn(total_timesteps=timesteps)
        self.model.save("learned_models/RLSnake_" + str(self.id))
        
    def load(self):
        self.model = DQN.load("learned_models/RLSnake_" + str(self.id))
        
    def get_action(self, obs):
        action, state = self.model.predict(obs)
        return action


   

  
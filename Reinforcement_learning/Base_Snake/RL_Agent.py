import numpy as np
from stable_baselines3 import DQN
from stable_baselines3 import PPO
from stable_baselines3 import A2C

class RL_Agent:
    
    def __init__(self, id):
        self.id = id
        
    def train_existing_model(self, env, timesteps):
        custom_objects = {"exploration_initial_eps": 1.0, "exploration_final_eps": 0.05, "exploration_fraction": 0.1}
        self.model = DQN.load("learned_models/RLSnake_" + str(self.id), env=env, custom_objects=custom_objects, verbose=0)       
        self.model.learn(timesteps)
        self.model.save("learned_models/RLSnake_" + str(self.id))

    def train(self, env, timesteps):
        self.model = DQN("MlpPolicy", env, verbose=0, learning_rate=0.005, tensorboard_log="tensorboard_logs/RLSnake/" + str(self.id), exploration_initial_eps=1, exploration_final_eps=0, exploration_fraction=0.2)
        #self.model  = DQN('MlpPolicy',  env, verbose=1, learning_rate=0.005, tensorboard_log="tensorboard_logs/RLSnake/" + str(self.id))
        self.model.learn(total_timesteps=timesteps)
        self.model.save("learned_models/RLSnake_" + str(self.id))
        
    def load(self):
        self.model = DQN.load("learned_models/RLSnake_" + str(self.id))
        
    def get_action(self, obs):
        action, state = self.model.predict(obs)
        return action


   

  
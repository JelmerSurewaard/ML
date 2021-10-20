import numpy as np
import tensorflow as tf
from stable_baselines import DQN
from stable_baselines import PPO2
from stable_baselines.common.schedules import LinearSchedule
from stable_baselines.common.vec_env import DummyVecEnv

class RL_Agent:
    
    def __init__(self, id, final_expo_rate):
        self.id = id
        self.final_expo_rate = final_expo_rate
        
    def train_existing_model(self, env, timesteps):
        custom_objects = {"exploration_initial_eps": 0.1, "exploration_final_eps": self.final_expo_rate, "exploration_fraction": 0.1}
        self.model = DQN.load("learned_models/RLSnake_" + str(self.id), custom_objects=custom_objects)       
        self.model.set_env(env)
        self.model.learn(timesteps)
        self.model.save("learned_models/RLSnake_" + str(self.id))

    def train(self, env, timesteps):
        policy_kwargs = dict(act_fun=tf.nn.relu, net_arch=[128,128])

        #self.model = DQN("MlpPolicy", env, verbose=1, learning_rate=0.005, tensorboard_log="./tensorboard_logs/RLSnake/", exploration_final_eps=final_expo_rate, exploration_initial_eps=1, exploration_fraction=0.2)
        self.model = PPO2("MlpPolicy", env, verbose=1, policy_kwargs=policy_kwargs, learning_rate=LinearSchedule( 40000 * 5, initial_p=0.0005, final_p=0.00005).value, tensorboard_log="./tensorboard_logs/RLSnake/")

        self.model.learn(total_timesteps=timesteps, tb_log_name=self.id)
        self.model.save("learned_models\RLSnake_" + str(self.id))
        
    def load(self):
        self.model = PPO2.load("learned_models/RLSnake_" + str(self.id))

    def train_exist_ppo(self, env, timesteps):
        snake_env = DummyVecEnv([lambda: env])
        self.model = PPO2.load("learned_models/RLSnake_" + str(self.id), verbose=1, tensorboard_log="./tensorboard_logs/RLSnake/")
        self.model.set_env(snake_env)
        self.model.learn(timesteps)
        self.model.save("learned_models/RLSnake_" + str(self.id))
        
    def get_action(self, obs):
        action, state = self.model.predict(obs)
        return action


   

  
import gym
import abides_gym

#import abides gym 
env = gym.make(
        "markets-execution-v0",
        background_config="rmsc04"
    )
#set the general seed
env.seed(0)

import ray
from ray import tune

from ray.tune.registry import register_env
# import env 

from abides_gym.envs.markets_execution_environment_v0 import (
    SubGymMarketsExecutionEnv_v0,
)

ray.init()


"""
DQN's default:
train_batch_size=32, sample_batch_size=4, timesteps_per_iteration=1000 -> workers collect chunks of 4 ts and add these to the replay buffer (of size buffer_size ts), then at each train call, at least 1000 ts are pulled altogether from the buffer (in batches of 32) to update the network.
"""
register_env(
    "markets-execution-v0",
    lambda config: SubGymMarketsExecutionEnv_v0(**config),
)

# algorithm, network architecture, hyperparameters
tune.run(
    "DQN",
    name="dqn_training",
    #"PPO",
    #name="ppo_training",
    resume=False,
    stop={"training_iteration": 100},  
    checkpoint_at_end=True,
    checkpoint_freq=5,
    config={
        "env": "markets-execution-v0",
        "env_config": {"background_config":"rmsc04",
                        "timestep_duration":"10S",
                        "execution_window": "04:00:00",
                        "parent_order_size": 20000,
                        "order_fixed_size": 50,
                        "not_enough_reward_update":-100,#penalty
            },
        "seed": tune.grid_search([1, 2, 3]),
        "num_gpus": 0,
        "num_workers": 0,
        "hiddens": [50, 20],
        "gamma": 1,
        "lr": tune.grid_search([0.001,0.0001, 0.01]),
        "framework": "torch",
        "observation_filter": "MeanStdFilter",
    },
)

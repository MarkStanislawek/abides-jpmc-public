import ray
from ray import tune

from abides_gym.envs.markets_daily_investor_environment_v0 import (
    SubGymMarketsDailyInvestorEnv_v0,
)

ray.init()

tune.run(
    "DQN",
    name="dqn_training",
    stop={"training_iteration": 200},  # train 200k steps
    checkpoint_freq=40,  # snapshot model every 40k steps
    config={  # Environment Specification
        "env": SubGymMarketsDailyInvestorEnv_v0,  # env used
        "env_config": {
            "order_fixed_size": 100,  # 1min wakeup frequency
            "timestep_duration": "60S", #{"seconds": 1 * 60},
        },
        "seed": tune.grid_search(
            [1, 2, 3]
        ),  # 3 seeds # Learning algorithm specification
        "hiddens": [50, 20],
        "gamma": 1,  # no discounting
    },
)

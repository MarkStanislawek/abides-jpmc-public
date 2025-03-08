import gym
import abides_gym


# 1) how to customize the environment config, i.e. timestep duration, execution window, parent order, penalty, ... ?
# 2) how to make the child order size (potentially) vary on each step within an episode ?
# 3) how to expose the book within the state space ?
# 4) install abides-gym so that local changes are reflected, e.g. print ask book for debugging, step through code.

env = gym.make(
    #"markets-daily_investor-v0",
    "markets-execution-v0",
    background_config="rmsc04",
)


env.seed(0)
initial_state = env.reset()
print(env.action_space)
print(env.execution_window)
for i in range(10):
    state, reward, done, info = env.step(2) # 0 == cxl all + mkt, 1 == cxl all + lmt, 2 == no action
    print(state,reward,done,info)
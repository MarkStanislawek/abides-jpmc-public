# Plan
## Finalize experiment parameters
Determine reasonable values for the following parameters:
- $parentOrderSize$: Total size the agent has to execute (either buy or sell).
- $childOrderSize$: The size of the agent's order. (I.e. the number of units to buy or sell at $t$.)
- $timeWindow$: Time length the agent is given to proceed with parentOrderSize execution.
- $timestepDuration$: The amount of time elapsed between two actions (trading opportunities).
- $direction$: acquisition or liquidation (BUY or SELL)

The strategy will be to run a `TWAP` agent within the environment over 200 episodes and capture (for each episode):
- Total quantity traded and the ratio of twap qty traded as a ratio to total volume

1. From this we can assume the agent will trade some fraction of the traded amount over the time window using this to set parentOrderSize.
1. We can also observe how prices are evolving.

### Parameters
- $parentOrderSize$: 36000 
    - Parent order size as a percentage of total volume traded per episode $\approx 5.5$%
    - TWAP order size = 25 

- $childOrderSize$: 
    - 75
- $timeWindow$
    - 4 hours
- $timestepDuration$: 
    - 10 Seconds
    - 1440 trading opportunities
- $direction$: 
    - SELL

## Gather performance of baseline strategies
- TWAP
    - 200 episodes, 288,000 timesteps
    - $\mu_{reward}=-43.98$, $\sigma_{reward}=153.99$
    - Episode wins = 0.509, losses = 0.491, failures (constraint) = 0.165 (33 of 200)
- VWAP
- Almgren-Chriss

Determine how performance between models is to be compared:
- Episode rewards
- PnL
- GLR (gain-loss ratio)

## Implement and train individual agents
- Custom logger for training to gather pnl results.
- Model weights checkpoint / save in tune and the ability to reconstruct the trained agent.
- Grid search on order_fixed_size, 50,75,100

## Setup the ensemble
- Majority voting and tie-handling logic

## Test individual agents and ensemble performance
- Across multiple random seeds average metrics, and then compare

## Assess generalization
- Vary market conditions.  e.g. different background agent configurations.


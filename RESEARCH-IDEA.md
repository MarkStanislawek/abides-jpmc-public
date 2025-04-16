# RL Agent Ensemble for Optimal Execution

## Overview

This study aims to develop multiple reinforcement learning (RL) agents with varying algorithms and neural network architectures for the optimal trade execution problem. The agents will be trained within the ABIDES-Gym RMSC04 market simulation environment. After individual training, the agents will be assembled into an ensemble, and a majority voting consensus algorithm will be used to determine the action. The performance of the ensemble will be compared to the individual agents' performance.

## Objective
To acquire or liquidate a fixed number of units of a financial security within a fixed time horizon, while minimizing the risk of unfavorable price movements caused either by an agent's trading or an agent delaying trading.

## Environment
- **Environment:** ABIDES-gym 
- **Configuration:** RMSC04
  - **Background Agents:**
    - 1 Exchange Agent
    - 2 Market Maker Agents
    - 102 Value Agents
    - 12 Momentum Agents
    - 1000 Noise Agents

- **Experiment Parameters**
  - $parentOrderSize$: Total size the agent has to execute (either buy or sell).
  - $childOrderSize$: The size of the agent's order. (I.e. the number of units to buy or sell at $t$.)
  - $direction$: direction of the parentOrder (buy or sell).
  - $timeWindow$: Time length the agent is given to proceed with parentOrderSize execution.
  - $timestepDuration$: The amount of time elapsed between two actions (trading opportunities).
  - $entryPrice$ is the midPrice_t at the beginning of the episode
  - $nearTouch_t$ is the highest bidPrice if direction = buy else is the lowest askPrice
  - $penalty$: it is a signed constant penalty per non-executed share at the end of the timeWindow.


### State Space
The experimental agent perceives the market through the state representation:
        
  $$s(t)=( holdingsPct_t, timePct_t, differencePct_t, imbalance5_t, imbalanceAll_t, priceImpact_t, spread_t, directionFeature_t, R^{k}_t)$$
       
  where:
  - $holdingsPct_t = \frac{holdings_t}{parentOrderSize}$: the execution advancement
  - $timePct_t=\frac{t - startingTime}{timeWindow}$: the time advancement
  - $differencePct_t = holdingsPct_t - timePct_t$ 
  - $priceImpact_t = midPrice_t - entryPrice$
  - $imbalance5_t=\frac{bids \ volume}{ bids \ volume + asks \ volume}$ using the first 5 levels of the order book. Value is respectively set to $0, 1, 0.5$ for no bids, no asks and empty book.
  - $imbalanceAll$ uses all levels of the order book.
  - $spread_t=bestAsk_t-bestBid_t$
  - $directionFeature_t= midPrice_t-lastTransactionPrice_t$
  - $R^k_t=(r_t,...,r_{t-k+1})$ series of mid price differences, where $r_{t-i}=mid_{t-i}-mid_{t-i-1}$. It is set to 0 when undefined. By default $k=4$ 
  
### Action Space
  The environment allows for three simple actions: "MARKET ORDER", "DO NOTHING" and "LIMIT ORDER". They are defined as follow:
  - "MARKET ORDER": the agent places a market order of size $childOrderSize$ in the direction $direction$. (Instruction to buy or sell immediately at the current best available price)
  - "LIMIT ORDER": the agent places a limit order of size $childOrderSize$ in the direction $direction$ at the price level $nearTouch_t$. (Buy or sell only at a specified price or better, does not guarantee execution)
  - "DO NOTHING": no action is taken.

  Before sending a "MARKET ORDER" or a "LIMIT ORDER", the agent will cancel any living order still in the Order Book.

### Reward
  $$R_{total} = R_{slippage} + R_{Late Penalty} = R_{slippage} + \lambda \times Quantity_{NotExecuted}$$

  with: 
  - $ \lambda = penalty $

  We define the step reward (slippage reward componant) as:
  $$reward_t= \frac{PNL_t}{parentOrderSize}$$

  with:
  $$PNL_t = \sum_{o \in O_t } numside\cdot(entryPrice - fillPrice_{o})* quantity_{o}$$
      
  where $numside=1$ if direction is buy else $numside=-1$ and $O_t$ is the set of orders executed between step $t-1$ and $t$
      
  We also define an episode update reward that is computed at the end of the episode. Denoting $O^{episode}$ the set of all orders executed in the episode, it is defined as: 

  - 0 if $\sum_{o \in O^{episode}} quantity_{o} = parentOrderSize$
  - else $\frac{penalty \times | parentOrderSize - \sum_{o \in O^{episode}} quantity_{o} |}{parentOrderSize}$

## RL Algorithms and Neural Network Architectures

- **RL Algorithms:**  
  - SAC (Soft Actor-Critic)  
  - PPO (Proximal Policy Optimization)  
  - Rainbow DQN  
  - TD3 (Twin Delayed Deep Deterministic Policy Gradient)  
  - AlphaZero (Monte Carlo Tree Search-based RL)

- **Neural Network Architectures:**  
  - Fully Connected Networks (FCN)
  - Possible augmentation with Recurrent Neural Networks (RNN), LSTMs, or GRUs
  - Hyperparameter grid search for architecture configurations using Ray Tune

## Exploration vs. Exploitation

- **Strategy:** Epsilon-greedy
- **Epsilon Annealing:** Linearly decay from 1 to 0.1 over 10,000 steps

## Training Process

- **Environment Sampling:** Handled by ABIDES-gym
- **Data Randomness:** Multiple background agents (market makers, noise, momentum, value) to ensure robustness.
- **Agent Testing:** Each agent tested individually over 6 random seed values. The average reward across these tests will be calculated.
- **Ensemble Testing:** The ensemble will also be tested over 6 random seed values, and the average reward will be computed for comparison.

## Ensemble Decision-Making

- **Number of Agents:** Odd number of agents.
- **Consensus Algorithm:** Majority Voting
  - If a tie occurs (equal votes for multiple actions), the action is selected at random from the three possible options.
  - **Tie Tracking:** The percentage of ties will be tracked to analyze how often a consensus is reached.

## Stabilizing Training

- **Techniques:**  
  - Prioritized Experience Replay  
  - Target Networks  
  - Gradient Clipping (where applicable)

## Generalization and Robustness

- **Market Conditions:**  
  - The background agent environment can be varied (e.g. adjusting the number of market maker, noise, momentum, and value agents) to test agent generalization across different market scenarios.

## Logging and Visualization

- **Tools:**  
  - Use Ray RLlib and Ray Tune for inbuilt metric logging.
  - Enhance with custom study specific metrics
  - Integrate with TensorBoard for real-time visualization of performance.

## Scaling and Parallelization

- **Cloud VM Setup:**  
  - Initial experiments will be run on a single compute and memory optimized cloud VM.
  - Hyperparameter tuning will be distributed across multiple cores of the VM.

## Testing and Validation
- Incorporate baseline comparison with TWAP, VWAP, and possibly AC performance.
- Use common market metrics for comparison.  Consider:
  - Gain/Loss and Profit/Loss ratios (e.g. average profit vs average loss)
  - VWAP
  - Slippage and price improvement
  - Market impact

- **Backtesting (Future Consideration):**  
  - Perform backtests with historical market data in addition to the ABIDES-gym environment.

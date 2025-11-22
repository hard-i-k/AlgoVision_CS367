"""
modified_epsilon.py

Standalone helper to run the "modified epsilon-greedy" agent for the
10-armed non-stationary bandit. This file is intentionally separate
to avoid confusion with other agent implementations.

Place this file in the same folder as your existing `bandits.py`.
Run with:
    python modified_epsilon.py

Outputs (saved in the working directory):
  - modified_vs_baselines_avg_reward.png
  - modified_vs_baselines_fraction_optimal.png
"""

import random
import numpy as np
import matplotlib.pyplot as plt
from bandits import (
    NonStationaryBandit,
    epsilon_greedy_sample_avg,
    epsilon_greedy_constant_alpha,
)

# reproducibility
SEED = 42
random.seed(SEED)
np.random.seed(SEED)


def modified_epsilon_greedy(env, steps=10000, epsilon=0.1, alpha=0.1):
    """
    Modified epsilon-greedy for NON-STATIONARY bandits:
    - Uses a constant step-size (alpha) update so the agent can track drifting means.
    - epsilon controls exploration (choose random arm with prob epsilon).
    Returns (rewards_list, optimal_bool_list).
    """
    Q = np.zeros(env.k)
    rewards = []
    optimal = []

    for t in range(steps):
        env.step()  # non-stationary drift happens each time-step

        # select action
        if random.random() < epsilon:
            action = np.random.randint(0, env.k)
        else:
            action = int(np.argmax(Q))

        # observe reward and update with constant alpha
        r = env.pull(action)
        Q[action] += alpha * (r - Q[action])

        rewards.append(r)
        optimal.append(action == int(np.argmax(env.means)))

    return rewards, optimal


# Utility: run many independent runs and compute mean reward and fraction optimal
def avg_runs(env_class, agent_fn, runs=200, steps=10000, **kwargs):
    rewards_all = np.zeros((runs, steps))
    optimal_all = np.zeros((runs, steps))
    for i in range(runs):
        env = env_class()
        r, opt = agent_fn(env, steps=steps, **kwargs)
        rewards_all[i] = np.array(r)
        optimal_all[i] = np.array(opt, dtype=float)
    return rewards_all.mean(axis=0), optimal_all.mean(axis=0)


def run_comparison(runs=200, steps=10000, epsilon=0.1, alpha=0.1):
    print("Starting comparison runs (this may take a while)...")
    # sample-average agent (baseline, not suited for non-stationary)
    mean_r_sa, mean_opt_sa = avg_runs(NonStationaryBandit, epsilon_greedy_sample_avg,
                                      runs=runs, steps=steps, epsilon=epsilon)
    print("Sample-average runs done.")

    # constant alpha agent (baseline)
    mean_r_ca, mean_opt_ca = avg_runs(NonStationaryBandit, epsilon_greedy_constant_alpha,
                                      runs=runs, steps=steps, epsilon=epsilon, alpha=alpha)
    print("Constant-alpha runs done.")

    # modified epsilon-greedy (function here)
    mean_r_mod, mean_opt_mod = avg_runs(NonStationaryBandit, modified_epsilon_greedy,
                                        runs=runs, steps=steps, epsilon=epsilon, alpha=alpha)
    print("Modified epsilon-greedy runs done.")

    # Plot average reward (cumulative average)
    steps_arr = np.arange(1, steps + 1)
    plt.figure(figsize=(8, 5))
    plt.plot(np.cumsum(mean_r_sa) / steps_arr, label='SampleAvg')
    plt.plot(np.cumsum(mean_r_ca) / steps_arr, label='ConstAlpha')
    plt.plot(np.cumsum(mean_r_mod) / steps_arr, label='ModifiedEpsGreedy')
    plt.xlabel("Steps")
    plt.ylabel("Average Reward (cumulative)")
    plt.title("10-Arm: Average Reward Comparison")
    plt.legend()
    plt.tight_layout()
    plt.savefig("modified_vs_baselines_avg_reward.png")
    plt.close()
    print("Saved modified_vs_baselines_avg_reward.png")

    # Plot fraction optimal action
    plt.figure(figsize=(8, 5))
    plt.plot(mean_opt_sa, label='SampleAvg')
    plt.plot(mean_opt_ca, label='ConstAlpha')
    plt.plot(mean_opt_mod, label='ModifiedEpsGreedy')
    plt.xlabel("Steps")
    plt.ylabel("Fraction Optimal Action")
    plt.title("10-Arm: Fraction Optimal Comparison")
    plt.legend()
    plt.tight_layout()
    plt.savefig("modified_vs_baselines_fraction_optimal.png")
    plt.close()
    print("Saved modified_vs_baselines_fraction_optimal.png")

    print("All done. Plots saved.")


if __name__ == "__main__":
    # reduce runs/steps for quick test; use larger for final (e.g., runs=200, steps=10000)
    run_comparison(runs=200, steps=10000, epsilon=0.1, alpha=0.1)

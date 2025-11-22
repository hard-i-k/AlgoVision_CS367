import matplotlib.pyplot as plt
import numpy as np
import random
import os

# reproducibility
SEED = 42
random.seed(SEED)
np.random.seed(SEED)

from bandits import (
    BinaryBandit,
    epsilon_greedy_bandit,
    NonStationaryBandit,
    epsilon_greedy_sample_avg,
    epsilon_greedy_constant_alpha,
    epsilon_greedy_constant_alpha_optimistic,
)

def run_binary_single():
    A = BinaryBandit([0.3, 0.6])
    rewards = epsilon_greedy_bandit(A, steps=1000, epsilon=0.1)
    plt.plot(np.cumsum(rewards) / np.arange(1, len(rewards) + 1))
    plt.xlabel("Steps")
    plt.ylabel("Average Reward")
    plt.title("Binary Bandit Average Reward (single run)")
    plt.savefig("binary_reward.png")
    plt.close()

# ---------- utilities to average across runs ----------
def avg_runs(env_class, agent_fn, runs=200, steps=10000, **kwargs):
    rewards_all = np.zeros((runs, steps))
    optimal_all = np.zeros((runs, steps))
    for i in range(runs):
        env = env_class()
        r, opt = agent_fn(env, steps=steps, **kwargs)
        rewards_all[i] = np.array(r)
        optimal_all[i] = np.array(opt, dtype=float)
    return rewards_all.mean(axis=0), optimal_all.mean(axis=0)

def run_10_arm_avg():
    steps = 10000
    runs = 200

    print("Running sample-average agent (this may take a while)...")
    mean_r1, mean_opt1 = avg_runs(NonStationaryBandit, epsilon_greedy_sample_avg, runs=runs, steps=steps, epsilon=0.1)

    print("Running constant-alpha agent...")
    mean_r2, mean_opt2 = avg_runs(NonStationaryBandit, epsilon_greedy_constant_alpha, runs=runs, steps=steps, epsilon=0.1, alpha=0.1)

    print("Running optimistic + constant-alpha agent...")
    mean_r3, mean_opt3 = avg_runs(NonStationaryBandit, epsilon_greedy_constant_alpha_optimistic, runs=runs, steps=steps, epsilon=0.1, alpha=0.1, Q0=5.0)

    # plot average reward curves
    plt.figure()
    plt.plot(np.cumsum(mean_r1) / np.arange(1, steps+1), label='SampleAvg')
    plt.plot(np.cumsum(mean_r2) / np.arange(1, steps+1), label='ConstAlpha')
    plt.plot(np.cumsum(mean_r3) / np.arange(1, steps+1), label='Optimistic+ConstAlpha')
    plt.xlabel('Steps')
    plt.ylabel('Avg Reward')
    plt.legend()
    plt.title('10-Arm: Average Reward Comparison')
    plt.savefig('10arm_avg_compare.png')
    plt.close()

    # plot % optimal action
    plt.figure()
    plt.plot(mean_opt1, label='SampleAvg')
    plt.plot(mean_opt2, label='ConstAlpha')
    plt.plot(mean_opt3, label='Optimistic+ConstAlpha')
    plt.xlabel('Steps')
    plt.ylabel('Fraction Optimal')
    plt.legend()
    plt.title('10-Arm: Fraction Optimal Action')
    plt.savefig('10arm_optimal_compare.png')
    plt.close()

    print("Saved 10-arm comparison plots.")

if __name__ == "__main__":
    if not os.path.exists("plots"):
        os.makedirs("plots")
    # move outputs into plots dir (optional)
    run_binary_single()
    run_10_arm_avg()
    print("All plots generated.")

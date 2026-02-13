import numpy as np

def monte_carlo(bankroll, win_prob, odds, stake_fraction, simulations=10000):
    ruin_count = 0
    for _ in range(simulations):
        capital = bankroll
        for _ in range(500):
            stake = capital * stake_fraction
            if np.random.rand() < win_prob:
                capital += stake*(odds-1)
            else:
                capital -= stake
            if capital <= 0:
                ruin_count += 1
                break
    return ruin_count/simulations

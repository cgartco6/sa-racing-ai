import numpy as np

def run_ai_predict(horses):
    predictions = []
    for h in horses:
        win_prob = np.random.uniform(0.3,0.8)  # ensemble placeholder
        stake_fraction = rl_suggest_fraction(win_prob)  # RL agent suggestion
        expected_return = simulate_bankroll(win_prob, stake_fraction)
        predictions.append({
            'name': h['name'],
            'jockey': h['jockey'],
            'trainer': h['trainer'],
            'win_prob': round(win_prob,2),
            'stake_fraction': round(stake_fraction,2),
            'expected_return': round(expected_return,2)
        })
    return predictions

def rl_suggest_fraction(win_prob):
    """Simple RL placeholder: higher prob → higher fraction"""
    if win_prob > 0.7:
        return 0.08
    elif win_prob > 0.5:
        return 0.05
    else:
        return 0.02

def simulate_bankroll(win_prob, stake_fraction, simulations=1000, odds=3.0):
    """Monte Carlo expected return"""
    returns = []
    for _ in range(simulations):
        result = np.random.rand() < win_prob
        if result:
            returns.append(stake_fraction * odds)
        else:
            returns.append(-stake_fraction)
    return np.mean(returns)

import numpy as np

class BettingRLAgent:
    def __init__(self, alpha=0.1):
        self.q_table = {}
        self.alpha = alpha

    def get_state(self, prob, odds):
        return (round(prob,2), round(odds,1))

    def choose_action(self, state):
        return np.random.choice(["bet","skip"])

    def update(self, state, reward):
        self.q_table[state] = self.q_table.get(state,0) + self.alpha*(reward - self.q_table.get(state,0))

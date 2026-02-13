def kelly_fraction(win_prob, odds, fraction=1):
    b = odds - 1
    q = 1 - win_prob
    f = (b*win_prob - q)/b
    return max(0,f) * fraction

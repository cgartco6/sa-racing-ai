def rank_race(model, race_df):
    probs = model.predict_proba(race_df)
    race_df["win_prob"] = probs
    race_df = race_df.sort_values("win_prob", ascending=False)
    return race_df

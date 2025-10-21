import pandas as pd
import joblib
import numpy as np
from datetime import datetime

# ==========================================
# 1️⃣ Load model and data
# ==========================================
model = joblib.load("models/pl_combined_model.joblib")
print("✅ Model loaded successfully.")

understat = pd.read_csv("data/understat_team_data.csv")
football = pd.read_csv("data/football_data_results.csv")
fixtures = pd.read_csv("data/pl_fixtures.csv")

# Standardize column names
understat.rename(columns={
    "team": "Team",
    "opponent": "Opponent",
    "date": "Date",
    "goals_for": "GF",
    "goals_against": "GA",
    "xG_for": "xG",
    "xG_against": "xGA",
}, inplace=True)

football.rename(columns={
    "Date": "Date",
    "HomeTeam": "HomeTeam",
    "AwayTeam": "AwayTeam",
    "B365H": "B365H",
    "B365D": "B365D",
    "B365A": "B365A"
}, inplace=True)

understat["Date"] = pd.to_datetime(understat["Date"], errors="coerce")
football["Date"] = pd.to_datetime(football["Date"], dayfirst=True, errors="coerce")
fixtures["date"] = pd.to_datetime(fixtures["date"], errors="coerce")

# ==========================================
# 2️⃣ Compute recent rolling averages
# ==========================================
stats_cols = ["xG", "xGA", "GF", "GA"]
for col in stats_cols:
    understat[f"{col}_rolling5"] = (
        understat.groupby("Team")[col].rolling(5, min_periods=1).mean().reset_index(0, drop=True)
    )

# ==========================================
# 3️⃣ Prepare helper function
# ==========================================
def get_latest_team_stats(team_name):
    """Return most recent rolling stats for a team."""
    team_data = understat[understat["Team"] == team_name].sort_values("Date")
    if team_data.empty:
        return None
    return team_data.iloc[-1]  # latest row

def get_latest_odds(home_team, away_team):
    """Fetch the most recent odds matchup between the two teams."""
    odds_row = football[
        (football["HomeTeam"] == home_team) & (football["AwayTeam"] == away_team)
    ].sort_values("Date")
    if not odds_row.empty:
        return odds_row.iloc[-1]
    # fallback: use mean odds
    return football[["B365H", "B365D", "B365A"]].mean()

# ==========================================
# 4️⃣ Predict fixtures
# ==========================================
predictions = []
pred_map = {2: "Home Win", 1: "Draw", 0: "Away Win"}

for _, fixture in fixtures.iterrows():
    home_team = fixture["home_team"]
    away_team = fixture["away_team"]

    home_stats = get_latest_team_stats(home_team)
    away_stats = get_latest_team_stats(away_team)
    odds = get_latest_odds(home_team, away_team)

    if home_stats is None or away_stats is None:
        print(f"⚠️ Skipping {home_team} vs {away_team} — missing stats.")
        continue

    # Compute feature differences
    feature_dict = {
        "xG_diff": home_stats["xG"] - away_stats["xG"],
        "xGA_diff": home_stats["xGA"] - away_stats["xGA"],
        "GF_diff": home_stats["GF"] - away_stats["GF"],
        "GA_diff": home_stats["GA"] - away_stats["GA"],
        "xG_rolling5_diff": home_stats["xG_rolling5"] - away_stats["xG_rolling5"],
        "xGA_rolling5_diff": home_stats["xGA_rolling5"] - away_stats["xGA_rolling5"],
        "B365H_prob": 1 / odds["B365H"] if odds["B365H"] > 0 else 0,
        "B365D_prob": 1 / odds["B365D"] if odds["B365D"] > 0 else 0,
        "B365A_prob": 1 / odds["B365A"] if odds["B365A"] > 0 else 0,
    }

    feature_dict["B365_diff"] = feature_dict["B365H_prob"] - feature_dict["B365A_prob"]

    feature_order = [
        "xG_diff", "xGA_diff", "GF_diff", "GA_diff",
        "xG_rolling5_diff", "xGA_rolling5_diff",
        "B365H_prob", "B365D_prob", "B365A_prob", "B365_diff"
    ]

    X_fixture = np.array([feature_dict[f] for f in feature_order]).reshape(1, -1)
    pred_code = model.predict(X_fixture)[0]
    pred_label = pred_map[pred_code]

    predictions.append({
        "date": fixture["date"],
        "home_team": home_team,
        "away_team": away_team,
        "predicted_result": pred_label
    })

# ==========================================
# 5️⃣ Save and display predictions
# ==========================================
pred_df = pd.DataFrame(predictions)
pred_df.to_csv("predictions/pl_upcoming_predictions.csv", index=False)
print("\n✅ Predictions saved to predictions/pl_upcoming_predictions.csv\n")
print(pred_df)

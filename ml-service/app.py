from flask import Flask, request, jsonify
import pandas as pd
import joblib
from scrapers.run_all_scrapers import run_all

app = Flask(__name__)

model = joblib.load("models/pl_combined_model.joblib")
understat = pd.read_csv("data/understat_team_data.csv")
football = pd.read_csv("data/football_data_results.csv")
fixtures = pd.read_csv("data/pl_fixtures.csv")

understat.rename(columns={
    "team": "Team",
    "opponent": "Opponent",
    "date": "Date",
    "goals_for": "GF",
    "goals_against": "GA",
    "xG_for": "xG",
    "xG_against": "xGA",
}, inplace=True)

understat["Date"] = pd.to_datetime(understat["Date"], errors="coerce")
football["Date"] = pd.to_datetime(football["Date"], dayfirst=True, errors="coerce")
fixtures["date"] = pd.to_datetime(fixtures["date"], errors="coerce")

# Compute rolling averages
for col in ["xG", "xGA", "GF", "GA"]:
    understat[f"{col}_rolling5"] = (
        understat.groupby("Team")[col].rolling(5, min_periods=1).mean().reset_index(0, drop=True)
    )

# Helper functions
def get_latest_team_stats(team_name):
    team_data = understat[understat["Team"] == team_name].sort_values("Date")
    return None if team_data.empty else team_data.iloc[-1]

def get_latest_odds(home_team, away_team):
    odds_row = football[
        (football["HomeTeam"] == home_team) & (football["AwayTeam"] == away_team)
    ].sort_values("Date")
    if not odds_row.empty:
        return odds_row.iloc[-1]
    return football[["B365H", "B365D", "B365A"]].mean()

@app.route("/scrape", methods=["GET"])
def scrape_data():
    """Run all scrapers and return summary of results"""
    try:
        results = run_all()
        return jsonify({
            "status": "success",
            "data": results
        })
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
    

@app.route("/predict", methods=["GET"])
def predict_fixtures():
    predictions = []
    pred_map = {2: "Home Win", 1: "Draw", 0: "Away Win"}

    for _, fixture in fixtures.iterrows():
        home_team = fixture["home_team"]
        away_team = fixture["away_team"]

        home_stats = get_latest_team_stats(home_team)
        away_stats = get_latest_team_stats(away_team)
        odds = get_latest_odds(home_team, away_team)

        if home_stats is None or away_stats is None:
            continue

        # Build features
        features = {
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
        features["B365_diff"] = features["B365H_prob"] - features["B365A_prob"]

        feature_order = [
            "xG_diff", "xGA_diff", "GF_diff", "GA_diff",
            "xG_rolling5_diff", "xGA_rolling5_diff",
            "B365H_prob", "B365D_prob", "B365A_prob", "B365_diff"
        ]
        X_fixture = np.array([features[f] for f in feature_order]).reshape(1, -1)

        # Predict result and probabilities
        probs = model.predict_proba(X_fixture)[0]
        pred_code = model.predict(X_fixture)[0]

        predictions.append({
            "home_team": home_team,
            "away_team": away_team,
            "predicted_result": pred_map[pred_code],
            "home_win_prob": round(probs[2] * 100, 1),
            "draw_prob": round(probs[1] * 100, 1),
            "away_win_prob": round(probs[0] * 100, 1)
        })

    return jsonify(predictions)


# @app.route("/predict", methods=["POST"])
# def predict():
#     if model is None:
#         return jsonify({"error": "No trained model found"}), 400

#     data = request.get_json()
#     df = pd.DataFrame(data)
#     preds = model.predict(df)
#     return jsonify({"predictions": preds.tolist()})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

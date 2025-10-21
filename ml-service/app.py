# from flask import Flask, request, jsonify
# import pandas as pd
# import joblib
# from scrapers.run_all_scrapers import run_all

# app = Flask(__name__)

# model = joblib.load("models/pl_combined_model.joblib")
# understat = pd.read_csv("data/understat_team_data.csv")
# football = pd.read_csv("data/football_data_results.csv")
# fixtures = pd.read_csv("data/pl_fixtures.csv")

# understat.rename(columns={
#     "team": "Team",
#     "opponent": "Opponent",
#     "date": "Date",
#     "goals_for": "GF",
#     "goals_against": "GA",
#     "xG_for": "xG",
#     "xG_against": "xGA",
# }, inplace=True)

# understat["Date"] = pd.to_datetime(understat["Date"], errors="coerce")
# football["Date"] = pd.to_datetime(football["Date"], dayfirst=True, errors="coerce")
# fixtures["date"] = pd.to_datetime(fixtures["date"], errors="coerce")

# # Compute rolling averages
# for col in ["xG", "xGA", "GF", "GA"]:
#     understat[f"{col}_rolling5"] = (
#         understat.groupby("Team")[col].rolling(5, min_periods=1).mean().reset_index(0, drop=True)
#     )

# # Helper functions
# def get_latest_team_stats(team_name):
#     team_data = understat[understat["Team"] == team_name].sort_values("Date")
#     return None if team_data.empty else team_data.iloc[-1]

# def get_latest_odds(home_team, away_team):
#     odds_row = football[
#         (football["HomeTeam"] == home_team) & (football["AwayTeam"] == away_team)
#     ].sort_values("Date")
#     if not odds_row.empty:
#         return odds_row.iloc[-1]
#     return football[["B365H", "B365D", "B365A"]].mean()

# @app.route("/scrape", methods=["GET"])
# def scrape_data():
#     """Run all scrapers and return summary of results"""
#     try:
#         results = run_all()
#         return jsonify({
#             "status": "success",
#             "data": results
#         })
#     except Exception as e:
#         import traceback
#         print(traceback.format_exc())
#         return jsonify({
#             "status": "error",
#             "message": str(e)
#         }), 500
    

# @app.route("/predict", methods=["GET"])
# def predict_fixtures():
#     predictions = []
#     pred_map = {2: "Home Win", 1: "Draw", 0: "Away Win"}

#     for _, fixture in fixtures.iterrows():
#         home_team = fixture["home_team"]
#         away_team = fixture["away_team"]

#         home_stats = get_latest_team_stats(home_team)
#         away_stats = get_latest_team_stats(away_team)
#         odds = get_latest_odds(home_team, away_team)

#         if home_stats is None or away_stats is None:
#             continue

#         # Build features
#         features = {
#             "xG_diff": home_stats["xG"] - away_stats["xG"],
#             "xGA_diff": home_stats["xGA"] - away_stats["xGA"],
#             "GF_diff": home_stats["GF"] - away_stats["GF"],
#             "GA_diff": home_stats["GA"] - away_stats["GA"],
#             "xG_rolling5_diff": home_stats["xG_rolling5"] - away_stats["xG_rolling5"],
#             "xGA_rolling5_diff": home_stats["xGA_rolling5"] - away_stats["xGA_rolling5"],
#             "B365H_prob": 1 / odds["B365H"] if odds["B365H"] > 0 else 0,
#             "B365D_prob": 1 / odds["B365D"] if odds["B365D"] > 0 else 0,
#             "B365A_prob": 1 / odds["B365A"] if odds["B365A"] > 0 else 0,
#         }
#         features["B365_diff"] = features["B365H_prob"] - features["B365A_prob"]

#         feature_order = [
#             "xG_diff", "xGA_diff", "GF_diff", "GA_diff",
#             "xG_rolling5_diff", "xGA_rolling5_diff",
#             "B365H_prob", "B365D_prob", "B365A_prob", "B365_diff"
#         ]
#         X_fixture = np.array([features[f] for f in feature_order]).reshape(1, -1)

#         # Predict result and probabilities
#         probs = model.predict_proba(X_fixture)[0]
#         pred_code = model.predict(X_fixture)[0]

#         predictions.append({
#             "home_team": home_team,
#             "away_team": away_team,
#             "predicted_result": pred_map[pred_code],
#             "home_win_prob": round(probs[2] * 100, 1),
#             "draw_prob": round(probs[1] * 100, 1),
#             "away_win_prob": round(probs[0] * 100, 1)
#         })

#     return jsonify(predictions)


# # @app.route("/predict", methods=["POST"])
# # def predict():
# #     if model is None:
# #         return jsonify({"error": "No trained model found"}), 400

# #     data = request.get_json()
# #     df = pd.DataFrame(data)
# #     preds = model.predict(df)
# #     return jsonify({"predictions": preds.tolist()})

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000)

from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
import joblib
import os
from pathlib import Path

app = Flask(__name__)

# Global variables
model = None
understat = None
football = None
fixtures = None

def load_data():
    """Load all data files with error handling"""
    global model, understat, football, fixtures
    
    errors = []
    
    # Load model
    model_path = "models/pl_combined_model.joblib"
    if not os.path.exists(model_path):
        errors.append(f"❌ Model not found at {model_path}")
        model = None
    else:
        try:
            model = joblib.load(model_path)
            print(f"✅ Model loaded from {model_path}")
        except Exception as e:
            errors.append(f"❌ Failed to load model: {e}")
            model = None
    
    # Load understat data
    understat_path = "data/understat_team_data.csv"
    if not os.path.exists(understat_path):
        errors.append(f"❌ Understat data not found at {understat_path}")
        understat = pd.DataFrame()
    else:
        try:
            understat = pd.read_csv(understat_path)
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
            
            # Compute rolling averages
            for col in ["xG", "xGA", "GF", "GA"]:
                understat[f"{col}_rolling5"] = (
                    understat.groupby("Team")[col]
                    .rolling(5, min_periods=1)
                    .mean()
                    .reset_index(0, drop=True)
                )
            print(f"✅ Understat data loaded: {len(understat)} rows")
        except Exception as e:
            errors.append(f"❌ Failed to load understat data: {e}")
            understat = pd.DataFrame()
    
    # Load football data
    football_path = "data/football_data_results.csv"
    if not os.path.exists(football_path):
        errors.append(f"❌ Football data not found at {football_path}")
        football = pd.DataFrame()
    else:
        try:
            football = pd.read_csv(football_path)
            football["Date"] = pd.to_datetime(football["Date"], dayfirst=True, errors="coerce")
            print(f"✅ Football data loaded: {len(football)} rows")
        except Exception as e:
            errors.append(f"❌ Failed to load football data: {e}")
            football = pd.DataFrame()
    
    # Load fixtures
    fixtures_path = "data/pl_fixtures.csv"
    if not os.path.exists(fixtures_path):
        errors.append(f"❌ Fixtures not found at {fixtures_path}")
        fixtures = pd.DataFrame()
    else:
        try:
            fixtures = pd.read_csv(fixtures_path)
            fixtures["date"] = pd.to_datetime(fixtures["date"], errors="coerce")
            print(f"✅ Fixtures loaded: {len(fixtures)} rows")
        except Exception as e:
            errors.append(f"❌ Failed to load fixtures: {e}")
            fixtures = pd.DataFrame()
    
    if errors:
        print("\n⚠️ Startup warnings:")
        for error in errors:
            print(error)
        print("\n💡 Run scrapers first: python -m scrapers.run_all_scrapers")
        print("💡 Or use the /scrape endpoint after starting the app\n")
    else:
        print("\n✅ All data loaded successfully!\n")
    
    return len(errors) == 0

# Helper functions
def get_latest_team_stats(team_name):
    if understat is None or understat.empty:
        return None
    team_data = understat[understat["Team"] == team_name].sort_values("Date")
    return None if team_data.empty else team_data.iloc[-1]

def get_latest_odds(home_team, away_team):
    if football is None or football.empty:
        return pd.Series({"B365H": 2.5, "B365D": 3.2, "B365A": 2.5})
    
    odds_row = football[
        (football["HomeTeam"] == home_team) & (football["AwayTeam"] == away_team)
    ].sort_values("Date")
    
    if not odds_row.empty:
        return odds_row.iloc[-1]
    
    # Fallback: Use conservative neutral odds
    return pd.Series({"B365H": 2.5, "B365D": 3.2, "B365A": 2.5})

@app.route("/", methods=["GET"])
def home():
    """API documentation"""
    return jsonify({
        "name": "Premier League Match Predictor API",
        "version": "1.0",
        "endpoints": {
            "/": "This help page",
            "/health": "Check API health status",
            "/scrape": "Run all data scrapers",
            "/predict": "Get predictions for upcoming fixtures"
        }
    })

@app.route("/health", methods=["GET"])
def health_check():
    """Check if the API is running and data is loaded"""
    return jsonify({
        "status": "healthy",
        "model_loaded": model is not None,
        "data": {
            "understat_rows": len(understat) if understat is not None else 0,
            "football_data_rows": len(football) if football is not None else 0,
            "fixtures_count": len(fixtures) if fixtures is not None else 0
        }
    })

@app.route("/scrape", methods=["GET"])
def scrape_data():
    """Run all scrapers and return summary of results"""
    try:
        from scrapers.run_all_scrapers import run_all
        results = run_all()
        
        # Reload data after scraping
        load_data()
        
        return jsonify({
            "status": "success",
            "data": results
        })
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        return jsonify({
            "status": "error",
            "message": str(e),
            "traceback": traceback.format_exc()
        }), 500

@app.route("/predict", methods=["GET"])
def predict_fixtures():
    """Get predictions for all upcoming fixtures"""
    
    # Validation
    if model is None:
        return jsonify({
            "error": "Model not loaded. Run /scrape first or train the model."
        }), 400
    
    if fixtures is None or fixtures.empty:
        return jsonify({
            "error": "No fixtures loaded. Run /scrape first."
        }), 400
    
    if understat is None or understat.empty:
        return jsonify({
            "error": "No understat data loaded. Run /scrape first."
        }), 400
    
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
            predictions.append({
                "home_team": home_team,
                "away_team": away_team,
                "error": "Missing team statistics"
            })
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
            "date": str(fixture["date"]),
            "home_team": home_team,
            "away_team": away_team,
            "predicted_result": pred_map[pred_code],
            "home_win_prob": round(probs[2] * 100, 1),
            "draw_prob": round(probs[1] * 100, 1),
            "away_win_prob": round(probs[0] * 100, 1)
        })

    return jsonify({
        "total_predictions": len(predictions),
        "predictions": predictions
    })

# Load data on startup
print("\n🚀 Starting Premier League Match Predictor API...")
load_data()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

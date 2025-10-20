import pandas as pd
import joblib
from datetime import datetime
import ast

# Load trained model
model = joblib.load("../models/pl_rf_model.joblib")
print("Model loaded successfully.")

# Load data
fixtures = pd.read_csv("../data/pl_fixtures.csv")
results = pd.read_csv("../data/football_data_results.csv")

# Convert JSON columns in past results
for col in ["ppda", "ppda_allowed"]:
    results[col] = results[col].apply(ast.literal_eval)

results = pd.concat([
    results.drop(columns=["ppda", "ppda_allowed"]),
    pd.json_normalize(results["ppda"]).add_prefix("ppda_"),
    pd.json_normalize(results["ppda_allowed"]).add_prefix("ppda_allowed_")
], axis=1)

results['date'] = pd.to_datetime(results['date'])
results['result_code'] = results['result'].map({'w': 2, 'd': 1, 'l': 0})

# Compute rolling_xG
results['rolling_xG'] = results.groupby('team')['xG'].rolling(3).mean().reset_index(0, drop=True)

# Define features
base_features = [
    "xG", "xGA", "npxG", "npxGA", "deep", "deep_allowed",
    "ppda_att", "ppda_def", "ppda_allowed_att", "ppda_allowed_def",
    "xpts", "npxGD", "rolling_xG"
]

predictions = []

for idx, row in fixtures.iterrows():
    home_team = row['home_team']
    away_team = row['away_team']
    
    try:
        home_stats = results[results['team'] == home_team].sort_values('date').iloc[-1]
        away_stats = results[results['team'] == away_team].sort_values('date').iloc[-1]
    except IndexError:
        print(f"Skipping fixture {home_team} vs {away_team}, missing stats.")
        continue

    # Create feature differences: home - away
    fixture_features = (home_stats[base_features] - away_stats[base_features]).values.reshape(1, -1)

    pred_code = model.predict(fixture_features)[0]
    pred_map = {2: "Home Win", 1: "Draw", 0: "Home Loss"}
    
    predictions.append({
        "date": row['date'],
        "home_team": home_team,
        "away_team": away_team,
        "predicted_result": pred_map[pred_code]
    })

pred_df = pd.DataFrame(predictions)
print(pred_df)

# Optional: save predictions
pred_df.to_csv("../predictions/pl_upcoming_predictions.csv", index=False)
print("Predictions saved to pl_upcoming_predictions.csv")

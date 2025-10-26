import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, TimeSeriesSplit, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import joblib
import warnings

import os

# Make sure the 'models' folder exists
os.makedirs("models", exist_ok=True)
warnings.filterwarnings("ignore")

# ==========================================
# 1️⃣ Load Data
# ==========================================
understat = pd.read_csv("../data/understat_team_data.csv")
football = pd.read_csv("../data/football_data_results.csv")

# Standardize column names
understat.rename(columns={
    "team": "Team",
    "opponent": "Opponent",
    "date": "Date",
    "goals_for": "GF",
    "goals_against": "GA",
    "xG_for": "xG",
    "xG_against": "xGA",
    "result": "Result"
}, inplace=True)

football.rename(columns={
    "Date": "Date",
    "HomeTeam": "HomeTeam",
    "AwayTeam": "AwayTeam",
    "FTHG": "HomeGoals",
    "FTAG": "AwayGoals",
    "FTR": "FTR"
}, inplace=True)

# Parse dates
understat["Date"] = pd.to_datetime(understat["Date"], errors="coerce")
football["Date"] = pd.to_datetime(football["Date"], dayfirst=True, errors="coerce")

# ==========================================
# 2️⃣ Compute rolling stats for Understat data
# ==========================================
stats_cols = ["xG", "xGA", "GF", "GA"]
for col in stats_cols:
    understat[f"{col}_rolling5"] = (
        understat.groupby("Team")[col].rolling(5, min_periods=1).mean().reset_index(0, drop=True)
    )

# ==========================================
# 3️⃣ Build Home/Away feature matrix
# ==========================================
# Merge Understat stats with Football-Data results
merged = football.merge(
    understat.add_prefix("home_"),
    left_on=["HomeTeam", "AwayTeam"],
    right_on=["home_Team", "home_Opponent"],
    how="left"
)

merged = merged.merge(
    understat.add_prefix("away_"),
    left_on=["AwayTeam", "HomeTeam"],
    right_on=["away_Team", "away_Opponent"],
    how="left"
)

# ==========================================
# 4️⃣ Feature Engineering
# ==========================================
merged["HomeWin"] = (merged["FTR"] == "H").astype(int)
merged["Draw"] = (merged["FTR"] == "D").astype(int)
merged["AwayWin"] = (merged["FTR"] == "A").astype(int)

merged["ResultCode"] = merged["FTR"].map({"H": 2, "D": 1, "A": 0})

# Compute differences (home - away)
for col in ["xG", "xGA", "GF", "GA", "xG_rolling5", "xGA_rolling5"]:
    merged[f"{col}_diff"] = merged[f"home_{col}"] - merged[f"away_{col}"]

# Betting odds features
for col in ["B365H", "B365D", "B365A"]:
    merged[col] = pd.to_numeric(merged[col], errors="coerce")

merged["B365H_prob"] = 1 / merged["B365H"]
merged["B365D_prob"] = 1 / merged["B365D"]
merged["B365A_prob"] = 1 / merged["B365A"]
merged["B365_diff"] = merged["B365H_prob"] - merged["B365A_prob"]

# ==========================================
# 5️⃣ Prepare training data
# ==========================================
feature_cols = [
    "xG_diff", "xGA_diff", "GF_diff", "GA_diff",
    "xG_rolling5_diff", "xGA_rolling5_diff",
    "B365H_prob", "B365D_prob", "B365A_prob", "B365_diff"
]

X = merged[feature_cols].fillna(0)
y = merged["ResultCode"]

# ==========================================
# 6️⃣ Train/Test Split & Model Training
# ==========================================
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

model = RandomForestClassifier(
    n_estimators=1000,
    max_depth=15,
    min_samples_split=5,
    class_weight="balanced",
    random_state=42
)
model.fit(X_train, y_train)

# ==========================================
# 7️⃣ Evaluation
# ==========================================
y_pred = model.predict(X_test)

print("\n📊 Classification Report:")
print(classification_report(y_test, y_pred))
print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

# Cross-validation (time-series safe)
tscv = TimeSeriesSplit(n_splits=5)
scores = cross_val_score(model, X, y, cv=tscv, scoring="accuracy")
print(f"\n⏱ Average CV accuracy: {scores.mean():.3f}")

# Feature importance
importances = model.feature_importances_
plt.figure(figsize=(10, 6))
plt.barh(feature_cols, importances)
plt.title("Feature Importances (Home - Away)")
plt.tight_layout()
plt.show()

# ==========================================
# 8️⃣ Save the trained model
# ==========================================
joblib.dump(model, "models/pl_combined_model.joblib")
print("\n✅ Model saved → models/pl_combined_model.joblib")

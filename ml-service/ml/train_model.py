import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import joblib
import ast

# ===============================
# 1️⃣ Load and preprocess data
# ===============================

results = pd.read_csv("../data/football_data_results.csv")

# Convert JSON columns
for col in ["ppda", "ppda_allowed"]:
    results[col] = results[col].apply(ast.literal_eval)

results = pd.concat([
    results.drop(columns=["ppda", "ppda_allowed"]),
    pd.json_normalize(results["ppda"]).add_prefix("ppda_"),
    pd.json_normalize(results["ppda_allowed"]).add_prefix("ppda_allowed_")
], axis=1)

results["date"] = pd.to_datetime(results["date"])
results["result_code"] = results["result"].map({'w': 2, 'd': 1, 'l': 0})

# Rolling average for recent form
results["rolling_xG"] = results.groupby("team")["xG"].rolling(3).mean().reset_index(0, drop=True)

# ===============================
# 2️⃣ Create home-away feature pairs
# ===============================

# Assume 'home_team' and 'away_team' columns exist
matches = results[["date", "team", "xG", "xGA", "npxG", "npxGA",
                   "deep", "deep_allowed", "ppda_att", "ppda_def",
                   "ppda_allowed_att", "ppda_allowed_def", "xpts", "npxGD", "rolling_xG"]]

# If your dataset has a 'match_id' or similar, group by it.
# Otherwise, join home/away manually using naming convention.
# We'll assume results has a 'team' and 'opponent' column.

if "opponent" not in results.columns:
    raise ValueError("Your dataset must include an 'opponent' column to pair matches.")

# Merge home and away rows from same match
merged = results.merge(
    results,
    left_on=["date", "team"],
    right_on=["date", "opponent"],
    suffixes=("_home", "_away")
)

# ===============================
# 3️⃣ Build difference features
# ===============================

base_features = [
    "xG", "xGA", "npxG", "npxGA", "deep", "deep_allowed",
    "ppda_att", "ppda_def", "ppda_allowed_att", "ppda_allowed_def",
    "xpts", "npxGD", "rolling_xG"
]

diff_features = [f"{feat}_diff" for feat in base_features]
for feat in base_features:
    merged[f"{feat}_diff"] = merged[f"{feat}_home"] - merged[f"{feat}_away"]

X = merged[diff_features]
y = merged["result_code_home"]

# ===============================
# 4️⃣ Train-test split and model
# ===============================

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, shuffle=False
)

model = RandomForestClassifier(
    n_estimators=500,
    max_depth=10,
    random_state=42
)
model.fit(X_train, y_train)

# ===============================
# 5️⃣ Evaluate model
# ===============================

y_pred = model.predict(X_test)
print("\nClassification Report:")
print(classification_report(y_test, y_pred))
print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))

# Feature importance
importances = model.feature_importances_
plt.figure(figsize=(10, 6))
plt.barh(diff_features, importances)
plt.xlabel("Importance")
plt.title("Feature Importance (Home - Away)")
plt.show()

# ===============================
# 6️⃣ Save model
# ===============================

joblib.dump(model, "../models/pl_home_away_model.joblib")
print("✅ Model saved as pl_home_away_model.joblib")

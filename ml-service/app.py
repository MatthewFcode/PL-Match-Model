from flask import Flask, jsonify
import pandas as pd
import google.generativeai as genai
import os

app = Flask(__name__)

genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
model = genai.GenerativeModel("models/gemini-pro-latest")
#client = genai.Client()

Predictions = "predictions/pl_upcoming_predictions.csv"
predictions_df = pd.read_csv(Predictions)

@app.route("/")
def get_predictions():
    """Return all predictions as JSON."""
    data = predictions_df.to_dict(orient="records")
    return jsonify(data)

if __name__ == "__main__": 
    app.run(debug=True)


@app.route("/predictions", methods=["GET"])
def enchance_predictions():
    
    csv_text = predictions_df.to_csv(index=False)
    prompt = f"""
    You are an expert Premier League data analyst.
    Review these predicted match results for accuracy and relevance:
    {csv_text}

    Instructions:
    - Check if any predictions seem unrealistic based on 2025 Premier League trends.
    - Suggest tweaks or corrections where necessary.
    - Return your response in structured JSON with fields:
      date, home_team, away_team, original_prediction, suggested_change, notes
    """

    response = model.generate_content(prompt)

    return jsonify({"gemini_review": response.text})
# @app.route("/gemini")
# def ask_gemini(): 
    
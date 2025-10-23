from flask import Flask, jsonify
import pandas as pd
import google.generativeai as genai
import os
import json 
import re

app = Flask(__name__)

genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
model = genai.GenerativeModel("models/gemini-flash-latest")
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
    - Returns all results even the ones that don't need changing and explains why that result is likely
    - Return your response in structured JSON with fields:
      date, home_team, away_team, winning_team, explanation

    Output requirements:
    - Return a **JSON array** (not text) where each match has its own object.
    - Use this exact JSON structure for each item:
      {{
          "date": "",
          "home_team": "",
          "away_team": "",
          "winning_team": "",
          "explanation": ""
      }}
    - winning_team needs to be the name of the team that wins not home win or away win
    - Ensure valid JSON syntax. Do not include explanations or text outside the array.
    """

    response = model.generate_content(prompt)

    response_text = response.text.strip()

    if response_text.startswith("```"):
        # Extract content between ```json and ```
        match = re.search(r'```(?:json)?\s*(\[.*\])\s*```', response_text, re.DOTALL)
        if match:
            response_text = match.group(1)
        else:
            # Fallback: remove all ``` markers
            response_text = re.sub(r'```(?:json)?', '', response_text).strip()
    
    try:
        # Parse the JSON to ensure it's valid
        predictions_data = json.loads(response_text)
        return jsonify(predictions_data)
    except json.JSONDecodeError as e:
        # If parsing fails, return the raw text for debugging
        return jsonify({
            "error": "Failed to parse JSON response",
            "details": str(e),
            "raw_response": response_text
        }), 500

    #return jsonify({"gemini_review": response.text})
# @app.route("/gemini")
# def ask_gemini(): 
    
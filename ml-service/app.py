from flask import Flask, request, jsonify
import pandas as pd
import joblib
from scrapers.fbref_scraper import scrape_fbref_premier_league

app = Flask(__name__)

# Load model
try:
    model = joblib.load("ml/model.pkl")
except:
    model = None
 
#  route that is getting data from the webscrapers
@app.route("/scrape", methods=["GET"])
def scrape_data():
    df = scrape_fbref_premier_league()
    return jsonify({"rows": len(df), "columns": list(df.columns)})

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    df = pd.DataFrame(data)
    preds = model.predict(df)
    return jsonify({"predictions": preds.tolist()})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
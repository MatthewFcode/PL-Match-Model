# from flask import Flask, request, jsonify
# import pandas as pd
# import joblib
# from scrapers.run_all_scrapers import run_all


# app = Flask(__name__)

# # Load model
# try:
#     model = joblib.load("ml/model.pkl")
# except:
#     model = None
 
# #  route that is getting data from the webscrapers

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

# @app.route("/predict", methods=["POST"])
# def predict():
#     data = request.get_json()
#     df = pd.DataFrame(data)
#     preds = model.predict(df)
#     return jsonify({"predictions": preds.tolist()})

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000)

# app.py
from flask import Flask, request, jsonify
import pandas as pd
import joblib
from scrapers.run_all_scrapers import run_all

app = Flask(__name__)

# Load model
try:
    model = joblib.load("ml/model.pkl")
    print("✅ ML model loaded successfully")
except:
    model = None
    print("⚠️ No model loaded yet — train one before using /predict")

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

@app.route("/predict", methods=["POST"])
def predict():
    if model is None:
        return jsonify({"error": "No trained model found"}), 400

    data = request.get_json()
    df = pd.DataFrame(data)
    preds = model.predict(df)
    return jsonify({"predictions": preds.tolist()})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

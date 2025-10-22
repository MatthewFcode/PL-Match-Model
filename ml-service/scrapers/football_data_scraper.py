import pandas as pd
import requests 
import io 

BASE_URL = "https://www.football-data.co.uk/mmz4281/2425/E0.csv"

def scrape_football_data(save=True):
    res = requests.get(BASE_URL)
    df = pd.read_csv(io.StringIO(res.text))
    cols = ["Date", "HomeTeam", "AwayTeam", "FTHG", "FTAG", "FTR", "B365H", "B365D", "B365A"]
    df = df[cols]
    if save: 
        df.to_csv("data/football_data_results.csv", index=False)
        print("✅ Saved Football-Data results → data/football_data_results.csv")
    return df

if __name__ == "__main__":
    scrape_football_data()

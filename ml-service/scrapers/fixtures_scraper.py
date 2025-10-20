import requests
import pandas as pd

BASE_URL = "https://footballapi.pulselive.com/football/fixtures?comps=1&teams=ALL&pageSize=1000"

def scrape_fixtures(save=True): 
  headers = {"Origin": "https://www.premierleague.com", "User-Agent": "Mozilla/5.0"}
  res = requests.get(BASE_URL, headers=headers)
  data = res.json()["content"]

  fixtures = []
  for f in data:
    fixtures.append({
       "homeTeam": f["teams"][0]["team"]["name"],
            "awayTeam": f["teams"][1]["team"]["name"],
            "kickoff": f["kickoff"]["label"],
            "gameweek": f["gameweek"]["gameweek"],
    })

    df = pd.DataFrame(fixtures)
    if save:
      df.to_csv("data/pl_fixtures.csv", index=False)
      print("✅ Saved fixtures → data/pl_fixtures.csv")
      return df
    
    if __name__ == "__main__":
      scrape_fixtures()
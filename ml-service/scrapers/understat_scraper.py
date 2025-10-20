import requests 
# re imports pythons regualr expression module | used to search for patterns in the HTML specifically to extract JSON embedded in JavaScript
import re
# json is used to parse strings into Python dictonaries/lists which is basically just a JS object
import json
import pandas as pd

BASE_URL = "https://understat.com/league/EPL"

# Scraping expected goals and shots and deep passes e.t.c
def scrape_understat_epl(save=True): 
  res = requests.get(BASE_URL)
  text = res.text
  json_data = re.search(r"var\s+teamsData\s+=\s+JSON.parse\('([^']+)'\)", text) # extracting JSON data from the text variable using regex | uses a regex pattern to capture the JSON data in the quotes | regex stands for regular expression
  if not json_data:
    raise Exception("❌ Could not extract team data from Understat.")
  json_data = json_data.group(1).encode('utf8').decode('unicode_escape') # group(1) gets the captured string for the regex search | encode and decode converts any escaped characters into proper unicode | making it valid JSON string ready to parse 
  teams_data = json.loads(json_data) # parsing the JSON into the python dictonary | teams_data is now a dictionary where keys are team IDs and values are team INFO

  teams = [] # list for all of the team data
  for team_id, team in teams_data.items(): # iterate over all the teams and get the match history 
    title = team["title"]
    history = pd.DataFrame(team['history'])
    history["team"] = title
    teams.append(history)

    df = pd.concat(teams, ignore_index=True) # concat all the different teams into one dataframe
    if save: 
      df.to_csv("data/understat_team_data.csv", index=False)
      print("✅ Saved Understat xG data → data/understat_team_data.csv")
      return df

if __name__ == "__main__":
    scrape_understat_epl()



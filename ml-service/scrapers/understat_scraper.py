# import asyncio
# import aiohttp
# import pandas as pd
# from understat import Understat

# async def scrape_understat_epl():
#     print("🚀 Scraping Understat team pages...")

#     async with aiohttp.ClientSession() as session:
#         understat = Understat(session)
#         league = "EPL"
#         season = 2024

#         teams = await understat.get_teams(league, season)
#         team_names = [team["title"] for team in teams]
#         print(f"✅ Found {len(team_names)} teams in {league}: {team_names}")

#         all_matches = []

#         for team in team_names:
#             print(f"📊 Fetching data for {team}...")
#             try:
#                 team_stats = await understat.get_team_results(team, season)
                
#                 if team_stats:
#                     # 👇 Print first match structure for inspection (optional)
#                     print(f"🔍 Example match structure for {team}:")
#                     print(team_stats[0])
                
#                 for match in team_stats:
#                     # Determine if this team was home or away
#                     is_home = match["side"] == "h"
#                     team_side = "h" if is_home else "a"
#                     opp_side = "a" if is_home else "h"

#                     all_matches.append({
#                         "team": match[team_side]["title"],
#                         "opponent": match[opp_side]["title"],
#                         "date": match["datetime"],
#                         "goals_for": float(match["goals"][team_side]),
#                         "goals_against": float(match["goals"][opp_side]),
#                         "xG_for": float(match["xG"][team_side]),
#                         "xG_against": float(match["xG"][opp_side]),
#                         "result": match["result"],
#                     })

#             except Exception as e:
#                 print(f"❌ Failed for {team}: {e}")

#         df = pd.DataFrame(all_matches)
#         df.to_csv("data/understat_team_data.csv", index=False)
#         print("✅ Saved Understat EPL data → data/understat_team_data.csv")
#         return df

# if __name__ == "__main__":
#     asyncio.run(scrape_understat_epl())
import asyncio
import aiohttp
import pandas as pd
import json
import re

BASE_URL = "https://understat.com/league/EPL/{}"  # season, e.g., 2024

async def fetch_page(session, url):
    async with session.get(url) as response:
        return await response.text()

async def scrape_understat_epl(season=2024):
    print(f"🚀 Scraping Understat EPL {season} data...")

    async with aiohttp.ClientSession() as session:
        html = await fetch_page(session, BASE_URL.format(season))

        # Look for any "JSON.parse('...')" in the page
        pattern = r"JSON\.parse\('(.+)'\)"
        matches = re.findall(pattern, html)
        if not matches:
            raise ValueError("Could not find JSON data in the page")

        # Usually the first match is the teams data
        data_str = matches[0].encode('utf-8').decode('unicode_escape')
        teams_data = json.loads(data_str)

        all_matches = []

        for team_id, team in teams_data.items():
            team_name = team["title"]
            for match_id, match in team["matches"].items():
                is_home = match["h"]["title"] == team_name
                team_side = "h" if is_home else "a"
                opp_side = "a" if is_home else "h"

                all_matches.append({
                    "team": match[team_side]["title"],
                    "opponent": match[opp_side]["title"],
                    "date": match["datetime"],
                    "goals_for": float(match["goals"][team_side]),
                    "goals_against": float(match["goals"][opp_side]),
                    "xG_for": float(match["xG"][team_side]),
                    "xG_against": float(match["xG"][opp_side]),
                    "result": match["result"]
                })

        df = pd.DataFrame(all_matches)
        df.to_csv(f"data/understat_epl_{season}.csv", index=False)
        print(f"✅ Saved Understat EPL data → data/understat_epl_{season}.csv")
        return df

if __name__ == "__main__":
    asyncio.run(scrape_understat_epl())

import asyncio
import aiohttp
import pandas as pd
from understat import Understat

async def test_scrape_understat_epl():
    print("🚀 Scraping Understat team pages...")

    async with aiohttp.ClientSession() as session:
        understat = Understat(session)
        league = "EPL"
        season = 2025

        teams = await understat.get_teams(league, season)
        team_names = [team["title"] for team in teams]
        print(f"✅ Found {len(team_names)} teams in {league}: {team_names}")

        all_matches = []

        for team in team_names:
            print(f"📊 Fetching data for {team}...")
            try:
                team_stats = await understat.get_team_results(team, season)
                
                if team_stats:
                    # 👇 Print first match structure for inspection (optional)
                    print(f"🔍 Example match structure for {team}:")
                    print(team_stats[0])
                
                for match in team_stats:
                    # Determine if this team was home or away
                    is_home = match["side"] == "h"
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
                        "result": match["result"],
                    })

            except Exception as e:
                print(f"❌ Failed for {team}: {e}")

        df = pd.DataFrame(all_matches)
        df.to_csv("data/understat_team_data.csv", index=False)
        print("✅ Saved Understat EPL data → data/understat_team_data.csv")
        return df

if __name__ == "__main__":
    asyncio.run(test_scrape_understat_epl())

# # #from scrapers.sofa_score_scraper import scrape_sofascore_standings
# # from scrapers.understat_scraper import scrape_understat_epl
# # from scrapers.football_data_scraper import scrape_football_data
# # from scrapers.fixtures_scraper import scrape_api_football_fixtures

# # def run_all():
# #     print("🚀 Starting all scrapers...")
    
# #     scrape_understat_epl()
# #     scrape_football_data()
# #     scrape_api_football_fixtures()
# #     #scrape_sofascore_standings()
# #     print("✅ All data sources refreshed.")

# # if __name__ == "__main__":
# #     run_all()
# from scrapers.understat_scraper import scrape_understat_epl
# from scrapers.football_data_scraper import scrape_football_data


# def run_all():
#     print("🚀 Starting all scrapers...")
    
#     results = {}
    
#     try:
#         df_understat = scrape_understat_epl()
#         results["understat"] = {
#             "status": "success",
#             "rows": len(df_understat),
#             "columns": list(df_understat.columns)
#         }
#     except Exception as e:
#         print(f"❌ Understat failed: {e}")
#         results["understat"] = {"status": "error", "message": str(e)}
    
#     try:
#         df_football_data = scrape_football_data()
#         results["football_data"] = {
#             "status": "success",
#             "rows": len(df_football_data),
#             "columns": list(df_football_data.columns)
#         }
#     except Exception as e:
#         print(f"❌ Football-Data failed: {e}")
#         results["football_data"] = {"status": "error", "message": str(e)}
    
#     # try:
#     #     df_fixtures = scrape_pl_fixtures()
#     #     results["api_football_fixtures"] = {
#     #         "status": "success",
#     #         "rows": len(df_fixtures),
#     #         "columns": list(df_fixtures.columns)
#     #     }
#     # except Exception as e:
#     #     print(f"❌ API-Football failed: {e}")
#     #     results["api_football_fixtures"] = {"status": "error", "message": str(e)}

#     print("✅ All data sources processed.")
#     return results

# if __name__ == "__main__":
#     run_all()
# scrapers/run_all_scrapers.py
import asyncio
from scrapers.understat_scraper import scrape_understat_epl
from scrapers.football_data_scraper import scrape_football_data

def run_all():
    print("🚀 Starting all scrapers...")
    results = {}

    try:
        # Run the async Understat scraper inside sync context
        df_understat = asyncio.run(scrape_understat_epl())
        results["understat"] = {
            "status": "success",
            "rows": len(df_understat),
            "columns": list(df_understat.columns)
        }
    except Exception as e:
        print(f"❌ Understat failed: {e}")
        results["understat"] = {"status": "error", "message": str(e)}

    try:
        df_football_data = scrape_football_data()
        results["football_data"] = {
            "status": "success",
            "rows": len(df_football_data),
            "columns": list(df_football_data.columns)
        }
    except Exception as e:
        print(f"❌ Football-Data failed: {e}")
        results["football_data"] = {"status": "error", "message": str(e)}

    print("✅ All data sources processed.")
    return results

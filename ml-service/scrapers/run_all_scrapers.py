# import asyncio
# # asyncio is pythons built in library for running asynchronous code
# from scrapers.football_data_scraper import scrape_football_data
# from scrapers.test_understat_scraper import test_scrape_understat_epl
# from scrapers.understat_scraper import scrape_understat_epl

# def run_all():
#     print("🚀 Starting all scrapers...")
#     results = {}

#     try:
#         # Run the async Understat scraper inside sync context
#         df_understat = asyncio.run(scrape_understat_epl())  # vairable defined with the scrape understat running asynchrnously 
#         results["understat"] = { # the data frame
#             "status": "success",
#             "rows": len(df_understat),
#             "columns": list(df_understat.columns)
#         }
#     except Exception as e:
#         print(f"❌ Understat failed: {e}")
#         results["understat"] = {"status": "error", "message": str(e)}
    
#     try:
#         # Run the async Understat scraper inside sync context
#         df_understat = asyncio.run(test_scrape_understat_epl())  # vairable defined with the scrape understat running asynchrnously 
#         results["understat"] = { # the data frame
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

#     print("✅ All data sources processed.")
#     return results

# if __name__ == "__main__":
#   run_all()
import asyncio
from scrapers.football_data_scraper import scrape_football_data
from scrapers.understat_scraper import scrape_understat_epl

def run_all():
    print("🚀 Starting all scrapers...")
    results = {}

    # --- Understat EPL scraper ---
    try:
        df_understat = asyncio.run(scrape_understat_epl())  # async scraper
        results["understat"] = {
            "status": "success",
            "rows": len(df_understat),
            "columns": list(df_understat.columns)
        }
    except Exception as e:
        print(f"❌ Understat failed: {e}")
        results["understat"] = {"status": "error", "message": str(e)}

    # --- Football-Data scraper ---
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

if __name__ == "__main__":
    run_all()

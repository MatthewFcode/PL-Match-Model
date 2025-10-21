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

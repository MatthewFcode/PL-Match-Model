from fbref_scraper import scrape_fbref_premier_league
from understat_scraper import scrape_understat_epl
from football_data_scraper import scrape_football_data
from fixtures_scraper import scrape_fixtures

def run_all():
  print("🚀 Starting all scrapers...")
  scrape_fbref_premier_league()
  scrape_understat_epl()
  scrape_football_data()
  scrape_fixtures()
  print("✅ All data sources refreshed.")
  
  if __name__ == "__main__": 
    run_all()
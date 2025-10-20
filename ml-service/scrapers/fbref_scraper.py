# import requests 
# # beatuful soup is a tool for parsing HTML and XML documents | lets us navigate and search the HTML document easily by turning it into a node tree of HTML elements from the long string 
# from bs4 import BeautifulSoup
# # pandas are a data manipulation library that will be used to store the scraped table in a structured Data Frame basically just turning our scarped data into an easily readable table 
# import pandas as pd

# BASE_URL = "https://fbref.com/en/comps/9/Premier-League-Stats"

# #Scraping corem team stats e.g. matches, players, goals, possesion, cards e.t.c
# # function definition with an optional argument that controls whether the results get savec to a CSV file
# def scrape_fbref_premier_league(save=True): 
#   # sends the HTTP get request to the base url 
#    res = requests.get(BASE_URL) # res now has the servers response with the long HTML string
#    soup = BeautifulSoup(res.text, "html.parser") # res.text is the raw HTML content from the request | parses the HTML back to the tree structure
#    table = soup.find("table", {"id": "stats_standard"}) # searches the parsed HTML for the <table> tag with the id 
#    headers = [th.get_text(strip=True) for th in table.find("thead").find_all("th")][1:] # locates all table header sections for the column names then extracts the text from each header and remvoes extra whitespace | 1: skips the ffirst header because it is usually an index column 
#    rows = [] # prepares to store row data to collect all team stats 
#    for row in table.find("tbody").find_all("tr"): # finds all the rows of actual data ignoring header rows, extracting all td elements and gets their text } if cols: removes empty rows 
#        cols = [td.get_text(strip=True) for td in row.find_all("td")]
#        if cols:
#            rows.append(cols) # adds the rows to the rows array
#    df = pd.DataFrame(rows, columns=headers) # converts the list of rows into a table using the extracted heeaders as column names
#    if save: 
#        df.to_csv("data/fbref_team_stats.csv", index=False) # if save does equal true then the data gets stored to th CSV file |  index=false prevents the pandas from adding an unnesary index column
#        print("✅ Saved FBref Premier League stats → data/fbref_team_stats.csv")
#    return df

# # python files have a special variable called __name__ | is the file is run directly the name variable is set as fbref_scraper 
# # tells it to only run this function if the file is exectued directly // so the function won't run automatically once it is imported
# if __name__ == "__main__":
#     scrape_fbref_premier_league()

import requests 
from bs4 import BeautifulSoup
import pandas as pd

BASE_URL = "https://fbref.com/en/comps/9/Premier-League-Stats"

def scrape_fbref_premier_league(save=True): 
    res = requests.get(BASE_URL)
    soup = BeautifulSoup(res.text, "html.parser")
    table = soup.find("table", {"id": "stats_standard"})
    headers = [th.get_text(strip=True) for th in table.find("thead").find_all("th")][1:]
    rows = []
    for row in table.find("tbody").find_all("tr"):
        cols = [td.get_text(strip=True) for td in row.find_all("td")]
        if cols:
            rows.append(cols)
    df = pd.DataFrame(rows, columns=headers)
    if save: 
        df.to_csv("data/fbref_team_stats.csv", index=False)
        print("✅ Saved FBref Premier League stats → data/fbref_team_stats.csv")
    return df

if __name__ == "__main__":
    scrape_fbref_premier_league()
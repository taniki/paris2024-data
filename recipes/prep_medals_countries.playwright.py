# +
import pandas as pd
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import math

source = 'https://olympics.com/en/paris-2024/medals'

def get_medals(row):
    spans = row.find_all('span')
    return {
        'code': spans[1].text.strip(),
        'country': spans[2].text.strip(),
        'gold': int(spans[3].text.strip()),
        'silver': int(spans[4].text.strip()),
        'bronze': int(spans[5].text.strip())
    }

def get_rows(page_source):
    soup = BeautifulSoup(page_source, "html.parser")
    rows = soup.find_all('div', {'data-testid': 'noc-row'})
    return [get_medals(row) for row in rows]

with sync_playwright() as p:
    browser = p.firefox.launch(headless=True)  # Change to True for headless mode
    page = browser.new_page()
    page.goto(source)
    
    page.wait_for_selector('#onetrust-reject-all-handler')  # Wait for 5 seconds
    
    # Accept cookies or reject (replace with the appropriate selector if needed)
    page.click('#onetrust-reject-all-handler')
    
    # Get the initial scroll height
    height = page.evaluate("document.documentElement.scrollHeight")
    window_height = page.evaluate("window.innerHeight * 1/2")
    
    rows = []
    page.evaluate("window.scrollTo(0, 0)")
    
    for y in range(0, math.ceil(height / window_height)):
        page.evaluate(f"window.scrollTo(0, {y*window_height})")
        page.wait_for_timeout(1000)  # Give time for the page to load
        rows += get_rows(page.content())
    
    browser.close()

# Create a DataFrame with the collected data
medals_countries_wide = (
    pd.DataFrame(rows)
    .drop_duplicates(subset=['code'])
    .reset_index(drop=True)
)

# Save wide format data to CSV
medals_countries_wide.to_csv('../datasets/medal_countries.wide.auto.csv', index=False)

# Convert to long format and save to CSV
medals_countries_long = (
    medals_countries_wide
    .melt(
        id_vars=['code', 'country'],
        var_name='medal',
        value_name='quantity'
    )
)

medals_countries_long.to_csv('../datasets/medal_countries.long.auto.csv', index=False)

# Save country codes and names to CSV
medals_countries_wide[['code', 'country']].sort_values('code').to_csv('../extras/ioc_countries.auto.csv', index=False)

print(medals_countries_long)
# -



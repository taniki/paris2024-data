# +
import pandas as pd
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import math

source = 'https://olympics.com/en/paris-2024/medals/medallists'

def get_total(row):
    # print(row)
    spans = row.find_all('span')
    
    if (len(spans) == 0):
        return
    
    country = spans[0].text.strip()
    name = spans[1].text.strip()
    
    gold = int(spans[2].text.strip())
    silver = int(spans[3].text.strip())
    bronze = int(spans[4].text.strip())

    return {
        # 'code': spans[1].text.strip(),
        'code': country,
        'name': name,
        'gold': gold,
        'silver': silver,
        'bronze': bronze
    }


def parse_medal_row(row):
    # print(row)
    a = row.find_all('a')
    spans = row.find_all('span')
    # print(a)
    # print(spans)
    
    try:
        discipline = a[0].text.strip()
        event = a[1].text.strip()
        color = spans[0].text.strip()

        return {
            'discipline': discipline,
            'event': event,
            'color': color
        }
    except:
        return


def get_medals(row):
    # print(row)
    spans = row.find_all('span')
    
    if (len(spans) == 0):
        return
    
    country = spans[0].text.strip()
    name = spans[1].text.strip()
    medals = [ parse_medal_row(row) for row in row.find_all('div', { 'data-medal-detail-id' : True })]
    
    return {
        # 'code': spans[1].text.strip(),
        'code': country,
        'name': name,
        'medals': medals
    }

def get_rows(page_source):
    soup = BeautifulSoup(page_source, "html.parser")
    rows = soup.find_all('div', {'data-index': True })
    return [get_total(row) for row in rows]

def get_rows2(page_source):
    soup = BeautifulSoup(page_source, "html.parser")
    rows = soup.find_all('div', {'data-index': True })
    return [get_medals(row) for row in rows]

with sync_playwright() as p:
    browser = p.firefox.launch(headless=True)  # Change to True for headless mode
    page = browser.new_page()
    page.goto(source)
    
    print(page.evaluate("document.documentElement.scrollHeight"))
    
    page.click('button[id="onetrust-accept-btn-handler"]')
    page.click('button[title="Expand all rows"]')
    page.wait_for_timeout(1000)

    print(page.evaluate("document.documentElement.scrollHeight"))

    # Get the initial scroll height
    height = page.evaluate("document.documentElement.scrollHeight")
    window_height = page.evaluate("window.innerHeight * 1/3")
    
    medallists_total = []
    medals = []

    page.evaluate("window.scrollTo(0, 0)")
    
    y = 0
    
    while y*window_height < height:
    #for y in range(0, math.ceil(height / window_height)):
        height = page.evaluate("document.documentElement.scrollHeight")
        page.evaluate(f"window.scrollTo(0, {y*window_height})")
        #page.wait_for_timeout(200)
        #page.wait_for_timeout(1000)  # Give time for the page to load
        medallists_total += get_rows(page.content())
        medals += get_rows2(page.content())
        y += 1

    #print(medals)
    #page.wait_for_timeout(5000)
    browser.close()

medallist_df = (
    pd.DataFrame
    .from_records([ x for x in medallists_total if x != None ])
    .drop_duplicates()
)

print(medallist_df)

medallist_df.to_csv('../datasets/medallists.csv', index=False)


medals_df = (
    pd.DataFrame
    .from_records([ x for x in medals if x != None ])
    .explode('medals')
    .pipe(lambda df:
        df.join(df.medals.apply(pd.Series))
    )
    .drop('medals', axis=1)
    .drop_duplicates()
    .query('~discipline.isna()')
)

print(medals_df)

medals_df.to_csv('../datasets/medals.csv', index=False)
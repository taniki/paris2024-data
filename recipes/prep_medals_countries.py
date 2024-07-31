import pandas as pd
import requests
from bs4 import BeautifulSoup
import math
from time import sleep
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.action_chains import ActionChains

source = 'https://olympics.com/en/paris-2024/medals'

firefox_options = Options()
#firefox_options.add_argument("--headless")
webdriver_service = Service("/snap/bin/firefox.geckodriver")
driver = webdriver.Firefox(service=webdriver_service, options=firefox_options)

driver.get(source)

sleep(5)

driver.find_element(By.ID, 'onetrust-reject-all-handler').click()

height = int(driver.execute_script("return document.documentElement.scrollHeight"))

window_height = int(driver.execute_script("return window.innerHeight") *2/3)

driver.execute_script("window.scrollTo(0, 0)")


# +
def get_medals(row):
    spans = row.find_all('span')
    
    return {
        'code': spans[1].text,
        'country': spans[2].text,
        'gold': int(spans[3].text),
        'silver': int(spans[4].text),
        'bronze': int(spans[5].text)
    }


def get_rows():
    soup = BeautifulSoup(driver.page_source, "html.parser")
    rows = soup.find_all('div', { 'data-testid': 'noc-row'})
    
    
    return [ get_medals(row) for row in rows ]

#get_rows()

# +
rows = []

driver.execute_script("window.scrollTo(0, 0)")

for y in range(0, math.ceil(height / window_height)):
    driver.execute_script(f"window.scrollTo(0, {y*window_height})")
    
    rows += get_rows()

medals_countries_wide = (
    pd
    .DataFrame(rows)
    .drop_duplicates(subset=['code'])
    .reset_index(drop=True)
)


medals_countries_wide
# -

driver.close()

medals_countries_wide.to_csv('../datasets/medal_countries.wide.csv', index=False)

# +
medals_countries_long = (
    medals_countries_wide
    .melt(
        id_vars=['code', 'country'],
        var_name = 'medal',
        value_name = 'quantity'
    )
)

medals_countries_long
# -

medals_countries_long.to_csv('../datasets/medal_countries.long.csv', index=False)

medals_countries_wide[['code', 'country']].sort_values('code').to_csv('../extras/ioc_countries.csv', index=False)



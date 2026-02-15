import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By

URL = "https://store.steampowered.com/search/?supportedlang=english&filter=globaltopsellers&ndl=1"

CHART_LENGTH = 20

SCROLL_TIME = 0.5

driver = webdriver.Chrome()
driver.get(URL)

rows = []
seen = set()
rank = 1

time.sleep(2)

try:
    while len(rows)<CHART_LENGTH:
        for element in driver.find_elements(By.CSS_SELECTOR, "a.search_result_row"):
            appid = element.get_attribute("data-ds-appid")
            if not appid or appid in seen:
                continue

            title = element.find_element(By.CSS_SELECTOR, "span.title").text

            seen.add(appid)
            rows.append({
                "rank": rank,
                "appid": appid,
                "title": title,
                "steam_url": element.get_attribute("href")
            })
            rank += 1
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(SCROLL_TIME)
            if len(rows) == CHART_LENGTH:
                break
    driver.quit()
    df = pd.DataFrame(rows)
except:
    driver.quit()
    df = pd.DataFrame(rows)

with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
    print(df)
import sys, random, time, csv, re
from datetime import datetime, timedelta


import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import dateparser
import pandas as pd

folder = '/Users/cemkarahan/Desktop/Python_Projects/gmaps/test_output/'

def run(place_id: str, outfile: str) -> None:
    driver = launch_browser()
    try:
        url = f"https://www.google.com/maps/place/?q=place_id:{place_id}&hl=en"
        driver.get(url)
        open_reviews(driver)
        scroll_reviews(driver)
        reviews = parse_html(driver)
        if not reviews:
            sys.exit('Error - No reviews found.')
        save_csv(reviews, outfile)
    finally:
        driver.quit()

def launch_browser(headless: bool = True):
    opts = uc.ChromeOptions()
    opts.headless = headless
    prefs = {"intl.accept_languages": "en-US, en",
             "translate": {"enabled": False},}
    opts.add_experimental_option("prefs", prefs)
    opts.add_argument("--lang=en-US")
    # can pin version_main if needed: version_main = 126 ?
    return uc.Chrome(options = opts)



def open_reviews(driver, timeout = 10):
    WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[role='tablist']")))
    locator = (By.CSS_SELECTOR, "div[role='tablist'] > button:nth-of-type(2)")
    try:
        button = WebDriverWait(driver, timeout).until(EC.element_to_be_clickable(locator))
        button.click()
    except Exception as e:
        sys.exit(f"Error - Could not open reviews pane: {e}")

"""def scroll_reviews(driver, pause: float = 0.8):
    #scroll until reaching the bottom #  jsaction="focus:scrollable.focus; blur:scrollable.blur"
    pane = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "QA0Szd")))
    scrollables = pane.find_elements(By.CSS_SELECTOR, "div[jsaction*='scrollable.focus']")
    print('printing: ', scrollables)
    region = scrollables[-1]
    #selector = "div[jsaction*='scrollable.focus']"
    #region = pane.find_element(By.CSS_SELECTOR, selector) # WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
    last_h, same = 0, 0
    while True:
        driver.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight);", region)
        time.sleep(pause + random.random() * 0.4)
        new_h = driver.execute_script("return arguments[0].scrollHeight;", region)
        if new_h == last_h:
            same += 1
            if same > 3:
                break
        else:
            same = 0
            last_h = new_h
    print("OK - Scrolled through all reviews")"""

def scroll_reviews(driver, pause: float = 0.8):
    last_count = 0
    same = 0
    while True:
        cards = driver.find_elements(By.CSS_SELECTOR, "div.jftiEf.fontBodyMedium")
        count = len(cards)
        #If no new cards have appeared in a few iterations
        if count == last_count:
            same += 1
            if same > 3:
                break
        else:
            same = 0
            last_count = count
        
        # scroll the last card
        if cards:
            try:
                # try to scroll the last one
                driver.execute_script(
                    "arguments[0].scrollIntoView(true);",
                    cards[-1]
                )
            except StaleElementReferenceException:
                # element went stale—skip this iteration and retry
                continue
        time.sleep(pause + random.random() * 0.4)
    print("OK - Scrolled through all reviews")

def relative_to_date(rel_str: str) -> datetime:
    dt = dateparser.parse(rel_str, settings = {'RELATIVE_BASE': datetime.utcnow()})
    if not dt:
        return datetime.utcnow()
    m = re.match(r"(\d+)\s%(day|week|month|year)", rel_str)
    if m:
        qty, unit = int(m[1]), m[2]
        span = {"day": 1, "week": 7, "month": 30, "year": 365}[unit]
        dt -= timedelta(days = random.randint(0, span - 1))
    return dt


## Soup
def parse_html(driver) -> list[dict]:
    soup = BeautifulSoup(driver.page_source, "html.parser")
    cards = soup.select("div.jftiEf.fontBodyMedium")
    reviews = soup.select('span.wiI7pd')
    out = []
    for c, r in zip(cards, reviews):
        out.append({'user_name': c['aria-label'],
                    'user_review': r.get_text(strip = True)})
    return out

def save_csv(data: list[dict], outfile: str):
    pd.DataFrame(data).to_csv(outfile, index=False, quoting=csv.QUOTE_ALL)
    print(f"[OK] Saved {len(data)} reviews to {outfile}")





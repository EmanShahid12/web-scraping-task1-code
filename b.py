from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import time
options = Options()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--start-maximized")
options.add_argument("--disable-notifications")
driver = webdriver.Chrome(options=options)
url = "https://www.bloomberg.com/politics"
print(f"Opening {url}")
driver.get(url)
input(" Please solve CAPTCHA in browser (if shown), then press ENTER to continue...")
try:
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'article'))
    )
except:
    print("Still blocked or structure changed.")
    driver.quit()
    exit()


while True:
    try:
        load_more = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-testid="loadMoreButton"]'))
        )
        driver.execute_script("arguments[0].click();", load_more)
        print(" Loading more articles...")
        time.sleep(2)
    except:
        print(" No more articles to load.")
        break
articles = driver.find_elements(By.CSS_SELECTOR, 'article a[href*="/news/articles/"]')
print(f" Found {len(articles)} articles.")

results = []
for article in articles:
    try:
        title = article.text.strip()
        url = article.get_attribute("href")
        parent = article.find_element(By.XPATH, './../../../..')
        description_el = parent.find_element(By.CSS_SELECTOR, 'div[data-testid="summary"]')
        description = description_el.text.strip()
        if title and url and description:
            results.append([title, url, description])
    except:
        continue
if results:
    with open("bloomberg_politics.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Title", "URL", "Description"])
        writer.writerows(results)
    print(f"Saved {len(results)} articles to bloomberg_politics.csv")
else:
    print(" No valid articles found.")

driver.quit()

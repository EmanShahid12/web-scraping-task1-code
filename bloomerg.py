import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
options = Options()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--start-maximized")
driver = uc.Chrome(options=options)
print("Opening Bloomberg Politics...")
driver.get("https://www.bloomberg.com/politics")

time.sleep(10)
driver.save_screenshot("bloomberg_page.png")
print(" Screenshot saved as bloomberg_page.png")
try:
    articles = driver.find_elements(By.CSS_SELECTOR, "article a")
    data = []
    for article in articles:
        title = article.text.strip()
        url = article.get_attribute("href")
        if title and url:
            data.append({"title": title, "url": url})

    if not data:
        print(" No articles found. CAPTCHA might still be active.")
    else:
        df = pd.DataFrame(data)
        df.to_csv("bloomberg_politics.csv", index=False)
        print(" Data saved to bloomberg_politics.csv")
except Exception as e:
    print(" Error:", e)

driver.quit()

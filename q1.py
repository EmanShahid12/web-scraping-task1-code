from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

def scrape_bloomberg_combined_with_date():
    print(" Scraping Bloomberg with Selenium + BeautifulSoup (including Date)...")
    
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("user-agent=Mozilla/5.0")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        driver.get("https://www.bloomberg.com")
        time.sleep(5)

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        articles = soup.find_all('article')

        print(f"Found {len(articles)} articles.\n")

        for i, article in enumerate(articles, start=1):
            title_tag = article.find(['h1', 'h2', 'h3'])
            title = title_tag.get_text(strip=True) if title_tag else "No Title"

            link_tag = article.find('a', href=True)
            link = link_tag['href'] if link_tag else "#"
            full_link = link if link.startswith("http") else f"https://www.bloomberg.com{link}"

            date = "Date not found"
            time_tag = article.find('time')
            if time_tag:
                if time_tag.has_attr('datetime'):
                    date = time_tag['datetime']
                else:
                    date = time_tag.get_text(strip=True)
            else:
                data_time = article.get('data-time')
                if data_time:
                    date = data_time

            print(f"  Article {i}:")
            print(f"   Title: {title}")
            print(f"   URL: {full_link}")
            print(f"   Date: {date}\n")

        print(" Finished scraping Bloomberg with date info.")

    except Exception as e:
        print(f" Error: {e}")

    finally:
        driver.quit()

if __name__ == "__main__":
    scrape_bloomberg_combined_with_date()

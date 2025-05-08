import xlwings as xw
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time


def main():
    scrape_prices()  # Calls your existing function


def scrape_prices():
    # Set up Selenium
    chrome_options = Options()
   # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)  # Correct single options

    # Connect to Excel
    wb = xw.Book.caller()  # Gets the Excel file running this script
    sheet = wb.sheets['sheet1']  # Your data sheet name  #sheet = wb.sheets.active (3lshan yb2a dynamic)


        #define the compatitors in excel
    COMPETITOR_COLS = {
        1: ('B', 'C'),  # URL1/Price1
        2: ('D', 'E'),  # URL2/Price2
        3: ('F', 'G'),  # URL3/Price3
        4: ('H', 'I')
    }

    COMPETITOR_SELECTORS = {
        "alfrensia.com": "p.price bdi",
        "sigma-computer.com": "span.price-new",
        "elbadrgroupeg.store": ["div.product-price", "div.product-price-new"],
        "ram-technology.com": "div.current-price"
    }
               #loop for compatitors
    for comp_num, (url_col, price_col) in COMPETITOR_COLS.items():

        urls = sheet.range(f'{url_col}2:{url_col}100').value

        prices = [""] * len(urls)


        for index, url in enumerate(urls):  # Track cell position
         if url:
            try:
                driver.get(url)
                price = "Not found"
                for domain, selectors in COMPETITOR_SELECTORS.items():
                     if domain in url:
                        # Convert single selector to list for uniform handling
                        selector_list = [selectors] if isinstance(selectors, str) else selectors

                        for selector in selector_list:
                            try:
                                price_element = WebDriverWait(driver, 10).until(  # Shorter timeout for fallback
                                    EC.visibility_of_element_located((By.CSS_SELECTOR, selector)))
                                price = price_element.text.split()[0]
                                break  # Use first successful match
                            except:
                                continue  # Try next selector if current fails
                    break  # Exit domain loop if price found

                prices[index] = price  # Place price at correct index

            except Exception as e:
                prices[index] = "Error"
                print(f"Error scraping {url}: {e}")

    # Write prices (aligned with URLs)
         sheet.range(f'{price_col}2').options(transpose=True).value = prices
    driver.quit()

    wb.save()




    if __name__ == "__main__":
        xw.Book("PriceScraper.xlsm").set_mock_caller()
        main()  # This makes "Run Main" work,

import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from openpyxl import load_workbook
from flask import FLask, request, Flask

# flask
app = Flask(__name__)
@app.route('/')
def home():
    auth = request.authorization
    if not auth or auth.password != "JeezLovesAll":
        return "Unauthorized", 401
    return "Welcome to your private tool!"

# 1. Set up Selenium
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
wait = WebDriverWait(driver, 10)
# 2. Read Excel
df = pd.read_excel("product and prices.xlsx")


# 3. Scrape Price with Smart Waiting
 # competitor selector

 #el  new get_Price function
def get_price(url):
    try:
        driver.get(url)
        time.sleep(3)  # Allow page to load
        driver.execute_script("window.scrollTo(0, 500);")  # Trigger lazy-loading

        COMPETITOR_SELECTORS = {
            "alfrensia.com": "p.price bdi",
            "sigma-computer.com": "span.price-new",
            "elbadrgroupeg.store": "div.product-price",
        }
        # Determine which selector to use
        for domain, selector in COMPETITOR_SELECTORS.items():
            if domain in url:
                price_element = wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                )
                price = price_element.text.split()[0]
                return float(price.replace(",", ""))
        return None  # No matching competitor
    except:
        return None


    # 4. Update Prices for All Competitors
for index, row in df.iterrows():
    # Loop through each competitor URL (1, 2, 3)
    for i in range(1, 4):  # Adjust range if you have more than 3 competitors
        url_col = f"Competitor_URL{i}" if i > 1 else "Competitor_URL"
        price_col = f"Competitor_Price{i}" if i > 1 else "Competitor_Price"

        if url_col in df.columns:  # Check if column exists
            url = row[url_col]
            if pd.notna(url):  # Check if URL is not empty
                current_price = get_price(url)
                if current_price:
                    df.at[index, price_col] = current_price




# 5. Save & Quit
df.to_excel("updated_prices.xlsx", index=False)
wb = load_workbook("updated_prices.xlsx")
wb['Sheet1'].auto_filter.ref = "A1:B1"  # Adjust Z to your last column
wb.save("updated_prices.xlsx")
driver.quit()
print("Prices updated")



#def get_price(url):
  #  try:
    #    driver.get(url)
    #    time.sleep(3)  # Allow page to load (adjust if needed)
        # Scroll to price (triggers lazy-loading if any)
     #   driver.execute_script("window.scrollTo(0, 500);")
        # Wait for price element to appear
      #  price_element = wait.until(
        #    EC.presence_of_element_located((By.CSS_SELECTOR, "p.price bdi"))
      #  )
      #  price = price_element.text.split()[0]  # Extract "16,800"
      #  return float(price.replace(",", ""))  # Remove commas → 16800.0
  #  except:
     #   return None

# 4. Update Prices
#for index, row in df.iterrows():
    #current_price = get_price(row["Competitor_URL" , "Competitor_URL2" , "Competitor_URL3"])
    #if current_price:
     #   df.at[index, "Competitor_Price" , "Competitor_Price2" , "Competitor_Price3"] = current_price

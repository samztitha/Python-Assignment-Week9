from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

# Setup ChromeDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Open Myntra category page (example: Women Kurtis)
driver.get("https://www.myntra.com/women-kurtas-kurtis")
time.sleep(5)

# Scroll down slowly to load products dynamically
for _ in range(5):
    driver.execute_script("window.scrollBy(0, 2000)")
    time.sleep(2)

# Find product containers
products = driver.find_elements(By.CSS_SELECTOR, "li.product-base")

# Create empty lists to store data
names = []
prices = []
discounts = []
links = []

# Extract data
for prod in products:
    # Name
    name = prod.find_element(By.CSS_SELECTOR, "h4.product-product").text
    names.append(name)

    # Price
    price = prod.find_element(By.CSS_SELECTOR, "div.product-price > span").text
    prices.append(price)

    # Discount (if available)
    try:
        discount = prod.find_element(By.CSS_SELECTOR, "div.product-price > span.product-discount").text
    except:
        discount = "N/A"
    discounts.append(discount)

    # Product link
    link = prod.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
    links.append(link)

# Create a DataFrame
df = pd.DataFrame({
    "Product Name": names,
    "Price": prices,
    "Discount": discounts,
    "Product Link": links
})

# Save to CSV
df.to_csv("products_pandas.csv", index=False)
print("Scraping completed! Data saved as products_pandas.csv")

driver.quit()

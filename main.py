from pprint import pprint
import json
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time

chrome_driver_path = "C:\\Users\\Shaharabanu's\\Application\\chromedriver.exe"
service = ChromeService(executable_path=chrome_driver_path)
driver = webdriver.Chrome(service=service)

SHEETY_ENDPOINT = "https://api.sheety.co/31ce745ac0c6040284abe8b2457955b5/copyOfAmazonScraping/sheet1"
response = requests.get(url=SHEETY_ENDPOINT)
data = response.json()
sheet_data = data["sheet1"]
pprint(sheet_data)

list = []
for ele in range(0, 100):
    dict = {}
    country_code = sheet_data[ele]["country"]
    asin = sheet_data[ele]["asin"]
    url = f"https://www.amazon.{country_code}/dp/{asin}"
    driver.get(url)
    time.sleep(10)

    # Extracting Product Title
    try:
        title = driver.find_element(by=By.ID, value="productTitle")
        title_value = title.text.strip().replace(',', '')

    except NoSuchElementException:
        print(f"{url} not available")
        title = ""

    if title != "":
        # Extracting Product Image URL
        try:
            image = driver.find_element(by=By.CLASS_NAME, value="a-dynamic-image")
            image_url = image.get_attribute('src')
        except AttributeError:
            image_url = ""

        #Extracting product Price
        try:
            price_product = driver.find_element(by=By.XPATH, value="//*[@id='usedBuySection']/div[1]/div/span[2]")
            price = price_product.text
        except NoSuchElementException:
            try:
                price_symbol = driver.find_element(by=By.CLASS_NAME, value="a-price-symbol")
                print(price_symbol.text)
                price_whole = driver.find_element(by=By.CLASS_NAME, value="a-price-whole")
                price_fraction = driver.find_element(by=By.CLASS_NAME, value="a-price-fraction")
                price = f"{price_symbol.text}{price_whole.text}.{price_fraction.text}"
            except NoSuchElementException:
                try:
                    price_product = driver.find_element(by=By.XPATH,
                                                        value="//*[@id='a-autoid-1-announce']/span[2]")
                    price = price_product.text
                except AttributeError:
                    price = ""

        #Extracting Product Details
        try:
            product_details = driver.find_element(by=By.ID, value="prodDetails")
            product_details_value = product_details.text.replace('\n',',')
        except NoSuchElementException:
            try:
                product_details = driver.find_element(by=By.ID, value="detailBullets_feature_div")
                product_details_value = product_details.text.replace('\n', ',')
            except AttributeError:
                product_details_value = ""

        dict["Product_Title"] = title_value
        dict["Product_Image_URL"] = image_url
        dict["Price"] = price
        dict["Product_Details"] = product_details_value

    list.append(dict)
   
print(list)

final_data = json.dumps(list, indent=2)
# print(final_data)

with open("sample.json", "w") as outfile:
    outfile.write(final_data)

# Task_Amazon_Product_Details

The URL's are in the format of "https://www.amazon.{country}/dp/{asin}". The
country code and Asin parameters are in the CSV file
https://docs.google.com/spreadsheets/d/1BZSPhk1LDrx8ytywMHWVpCqbm8URT
xTJrIRkD7PnGTM/edit?usp=sharing.

Use Selenium I had scraped the following details from the page.
1. Product Title
2. Product Image URL
3. Price of the Product
4. Product Details
If any URL throws Error 404 then it will print, {URL} not available and skip that
URL.

The output are shown as a list of dictionaries and finally represented in JSON.

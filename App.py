from flask import Flask, render_template, request
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import random
import time

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    name = request.form['product_name']
    products = []

    # Get Flipkart product details
    flk_price, flk_link = flipkart(name)
    if flk_price:
        products.append({'platform': 'Flipkart', 'price': flk_price, 'link': flk_link})

    # Get Amazon product details
    amzn_price, amzn_link = amazon(name)
    if amzn_price:
        products.append({'platform': 'Amazon', 'price': amzn_price, 'link': amzn_link})

    # Sort products by price in ascending order
    products.sort(key=lambda x: x['price'])

    return render_template('search_results.html', products=products, product_name=name)

def flipkart(name):
    fkurl = f'https://www.flipkart.com/search?q={name}'
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        driver.get(fkurl)
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.s-main-slot')))
        time.sleep(random.uniform(2, 4))
        fksoup = BeautifulSoup(driver.page_source, 'html.parser')

        # Scraping logic for Flipkart
        product = fksoup.find('div', {'class': '_1AtVbE'})  # Adjust the selector as needed
        fk_price = product.find('div', {'class': '_30jeq3'}).text  # Adjust the selector as needed
        fk_link = product.find('a', {'class': 'IRpwTa'})['href']  # Adjust the selector as needed
        fk_link = f'https://www.flipkart.com{fk_link}'  # Complete the URL

    except Exception as e:
        print(f"An error occurred while scraping Flipkart: {e}")
        fk_price, fk_link = "0", None  # Return price as string
    finally:
        driver.quit()

    return fk_price, fk_link  # Return price as string

def amazon(name):
    amzurl = f'https://www.amazon.in/s?k={name}'
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        driver.get(amzurl)
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.s-main-slot')))
        time.sleep(random.uniform(2, 4))
        amz_soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Scraping logic for Amazon
        product = amz_soup.find('div', {'data-component-type': 's-search-result'})  # Adjust the selector as needed
        amz_price = product.find('span', {'class': 'a-price-whole'}).text  # Adjust the selector as needed
        amz_link = product.find('a', {'class': 'a-link-normal'})['href']  # Adjust the selector as needed
        amz_link = f'https://www.amazon.in{amz_link}'  # Complete the URL

    except Exception as e:
        print(f"An error occurred while scraping Amazon: {e}")
        amz_price, amz_link = "0", None  # Return price as string
    finally:
        driver.quit()

    return amz_price, amz_link  # Return price as string

def convert(price_str):
    # Convert price string to integer
    price_str = price_str.replace("₹", "").replace(",", "").strip()
    return int(price_str) if price_str.isdigit() else 0

if __name__ == '__main__':
    app.run(debug=True)


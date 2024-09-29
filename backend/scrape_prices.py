### This script is used to scrape the uberfarefinder.com website for the prices of Uber rides

import requests;
import pandas as pd;
from multiprocessing import Pool
import os;


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from bs4 import BeautifulSoup
import time

def get_uber_fare(start_location, end_location):
    # Set up the Selenium WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run in headless mode
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        # Navigate to the Uber Fare Finder website
        url = "https://uberfarefinder.com/"
        driver.get(url)

        # Input the start location
        start_input = driver.find_element(By.CSS_SELECTOR, "input[placeholder='Enter start location']")
        start_input.clear()
        start_input.send_keys(start_location)
        start_input.send_keys(Keys.RETURN)

        # Input the end location
        end_input = driver.find_element(By.CSS_SELECTOR, "input[placeholder='Enter end location']")
        end_input.clear()
        end_input.send_keys(end_location)
        end_input.send_keys(Keys.RETURN)

        # Submit the form
        try:
            submit_button = driver.find_element(By.ID, "get-fare-button")
            submit_button.click()
        except:
            time.sleep(10)
    

        # Wait for the results to load
        WebDriverWait(driver, 45).until(
            EC.presence_of_element_located((By.CLASS_NAME, "fare-finder-result"))
        )

        # Get the page source and parse it with BeautifulSoup
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')

        # Find the table inside the "fare-finder-result" div
        #fare_finder_div = soup.find('div', class_='fare-finder-result')
        #if fare_finder_div:
            #table = fare_finder_div.find('table')
            #return table
        tables = soup.find_all('td');
        return tables

    finally:
        driver.quit()

def append_to_file( file_path, data ):
    # if csv file does not exist, create it
    # uf it does exist, append to it
    if not os.path.isfile(file_path):
        data.to_csv(file_path, index=False)
    else:
        data.to_csv(file_path, mode='a', header=False, index=False)

def get_final_price( price_table ):
    for element in price_table:
        if "<td class=\"text-right\"><strong class=\"ng-binding\">$" in str(element):
            print(element);
            temp = str(element).split("$");
            temp = temp[1].split("<")[0];
            return temp;

def main( locations ):
    data = pd.DataFrame(columns=['date', 'time', 'start_location', 'end_location', 'total_price'])
    start_location = locations[0]
    end_location = locations[1]
    t = time.strftime("%H:%M:%S")
    
    price_table = get_uber_fare(start_location, end_location);
    total_price = get_final_price( price_table );
    data = data.append({'date': date, 'time': t, 'start_location': start_location, 'end_location': end_location, 'total_price': total_price}, ignore_index=True)
    filename = 'locational_prices.csv'
    append_to_file(filename, data)
    print(total_price)

    #time.sleep(300)


if __name__ == "__main__":
    #data = pd.DataFrame(columns=['date', 'time', 'start_location', 'end_location', 'total_price'])

    # loop to run this every 5 minutes for 1 hour
    date = time.strftime("%m/%d/%Y")
    start_time = time.time()

    start_location = "Yorkville, Toronto, Ontario, Canada"
    end_location = "Scotiabank Arena, 40 Bay St, Toronto, Ontario M5J 2X8, Canada"
    location1 = (start_location, end_location)

    start_location = "75 Queen's Park Cres E, Toronto, ON M5S 1K7, Canada"
    location2 = (start_location, end_location)

    start_location = "30 Hillsboro Ave, Toronto, ON M5R 1S7, Canada"
    location3 = (start_location, end_location)

    start_location = "86 Bedford Rd, Toronto, ON M5R 2K9, Canada"
    location4 = (start_location, end_location)

    start_location = "2 Bloor St E, Toronto, ON M4W 1A8, Canada"
    location5 = (start_location, end_location)

    start_location = "32 Davenport Rd, Toronto, ON M5R 0B5"
    location6 = (start_location, end_location)

    start_location = "127 Avenue Rd, Toronto, ON M5R 2H4"
    location7 = (start_location, end_location)

    start_location = "220 Bloor St W, Toronto, ON M5S 1T8"
    location8 = (start_location, end_location)

    start_location = "77 Bloor St W, Toronto, ON M5S 1M2"
    location9 = (start_location, end_location)

    with Pool(10) as p:
        p.map(main, [location1, location2, location3, location4, location5, location6, location7, location8, location9])
    
    end_time = time.time()
    print("Time taken: ", end_time - start_time)
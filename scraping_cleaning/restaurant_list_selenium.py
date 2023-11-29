from selenium import webdriver
import time
import sys

import numpy as np
import pandas as pd
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

columns_list = ['rest_name', 'rest_url', 'rating', 'n_reviews', 'top_tags_price', 'order_online', 'travellers_choice',
               'michelin']

def scrapeCityRestrauntList(list_url, columns_list, show_browser=False):
    def check_exists_by_css_selector(css_selector_string, sel_location=None):
        try:
            if sel_location is None:
                driver.find_element(By.CSS_SELECTOR, css_selector_string)
            else:
                sel_location.find_element(By.CSS_SELECTOR, css_selector_string)
        except NoSuchElementException:
            return False
        return True

    def scrapeRestrauntData(restaurant_data):
        scraped_data = []
        if check_exists_by_css_selector("div.tkvCJ", restaurant_data):
            restr_name = restaurant_data.find_element(By.CSS_SELECTOR, 'div.tkvCJ')
        else:
            restr_name = restaurant_data.find_element(By.CSS_SELECTOR, 'div.VDEXx')
        #restraunt name
        scraped_data.append(restr_name.text)
        #restraunt link (with id in it)
        scraped_data.append(restr_name.find_element(By.CSS_SELECTOR, 'a').get_attribute('href'))
        #restraunt average rating
        if check_exists_by_css_selector("svg.UctUV", restaurant_data):
            scraped_data.append(restaurant_data.find_element(By.CSS_SELECTOR, 'svg.UctUV').get_attribute('aria-label'))
        else:
            scraped_data.append('None')
        # number of reviews
        if check_exists_by_css_selector("span.IiChw", restaurant_data):
            scraped_data.append(restaurant_data.find_element(By.CSS_SELECTOR, 'span.IiChw').text)
        else:
            scraped_data.append('None')
        #both price range, top tags and menu
        if check_exists_by_css_selector("div.mIBqD", restaurant_data):
            scraped_data.append(restaurant_data.find_element(By.CSS_SELECTOR, 'div.mIBqD').text)
        elif check_exists_by_css_selector("div.FGSTQ"):
            scraped_data.append(restaurant_data.find_element(By.CSS_SELECTOR, 'div.FGSTQ').text)
        else:
            scraped_data.append('None')
        #order online
        if check_exists_by_css_selector('div.uWSwo', restaurant_data):
            scraped_data.append(restaurant_data.find_element(By.CSS_SELECTOR, 'div.uWSwo').text)
        else:
            scraped_data.append('None')
        #Traveller's choice
        if check_exists_by_css_selector('span.NAWmh', restaurant_data):
            scraped_data.append(restaurant_data.find_element(By.CSS_SELECTOR, 'span.NAWmh').text)
        else:
            scraped_data.append('None')
        #Michlen Star
        if check_exists_by_css_selector('div.SCHws', restaurant_data):
            scraped_data.append(restaurant_data.find_element(By.CSS_SELECTOR, 'div.SCHws').text)
        else:
            scraped_data.append('None')

        return scraped_data

    if show_browser:
        driver = webdriver.Chrome()
    else:
        options = webdriver.chrome.options.Options()
        options.add_argument("--headless")
        driver = webdriver.Chrome(options=options)
    driver.get(list_url)
    time.sleep(5)

    # Press the button to limit search only to restaurants in the city
    if check_exists_by_css_selector('.hXLiT'):
        button_zone = driver.find_element(By.CLASS_NAME, "hXLiT")
        button_itself = button_zone.find_element(By.CLASS_NAME, 'raEkE')
        button_itself.click()
        time.sleep(3)
    elif check_exists_by_css_selector('#geobroaden_opt_out'):
        button_zone = driver.find_element(By.CSS_SELECTOR, "#geobroaden_opt_out")
        if button_zone.is_displayed():
            button_zone.click()
        time.sleep(3)

    # Remove filters to show all restaurants
    if check_exists_by_css_selector('.XbzVv'):
        button_remove_filters = driver.find_element(By.CLASS_NAME, 'XbzVv')
        button_remove_filters.click()
        time.sleep(3)
    elif check_exists_by_css_selector('.ACvVd'):
        button_remove_filters = driver.find_element(By.CLASS_NAME, 'ACvVd')
        button_remove_filters.click()
        time.sleep(3)

    # Main cycle to click the next button, gather the data and click next again
    all_restaurant_data = []
    next_page_flag = True
    j = 0
    while next_page_flag:
        for i in range(1, 31):
            selector_string = '[data-test="' + str(i + j) + '_list_item"]'
            if check_exists_by_css_selector(selector_string):
                restaurant_data = driver.find_element(By.CSS_SELECTOR, selector_string)
                all_restaurant_data.append(scrapeRestrauntData(restaurant_data))

        if check_exists_by_css_selector('[data-smoke-attr="pagination-next-arrow"]'):
            next_button = driver.find_element(By.CSS_SELECTOR, '[data-smoke-attr="pagination-next-arrow"]')
            driver.execute_script("arguments[0].click();", next_button)
            #next_button.click()
            print('next button found ' + str(len(all_restaurant_data)))
            time.sleep(15)
        elif check_exists_by_css_selector('.next.ui_button'):
            next_button = driver.find_element(By.CSS_SELECTOR, '.next.ui_button')
            driver.execute_script("arguments[0].click();", next_button)
            #next_button.click()
            print('next button found ' + str(len(all_restaurant_data)))
            time.sleep(15)
        else:
            next_page_flag = False
        j += 30
        df = pd.DataFrame(all_restaurant_data, columns=columns_list)
        #df.to_csv('BG_by_city_backup.csv', index=False)

    driver.close()
    return all_restaurant_data

def scrape_list(url_list, save_path):
    df = pd.DataFrame(columns=columns_list)
    for url in url_list:
        list_data = scrapeCityRestrauntList(url, columns_list)
        df_i = pd.DataFrame(list_data, columns=columns_list)
        df = pd.concat([df, df_i])
        df.to_csv(save_path, index=False)
        time.sleep(15)

# Code used for testing in console
#df = pd.read_csv('NI_city_lists.csv')
#df = pd.read_csv('SK_city_lists.csv')
#df = pd.read_csv('BG_city_lists.csv')
#df = pd.read_csv('FI_city_lists.csv')
#url_list = list(df['url'])

#list_to_scrape = url_list[2:4]
#https://www.tripadvisor.com/FindRestaurants?geo=186470&offset=750&broadened=false

#driver = webdriver.Chrome()
#driver.get(url_list[0])

if __name__ == '__main__':
    csv_path = sys.argv[1]
    position = int(sys.argv[2])
    output_path = sys.argv[3]

    df_urls = pd.read_csv(csv_path)
    url_list = df_urls['url'].iloc[position:]
    scrape_list(url_list, output_path)
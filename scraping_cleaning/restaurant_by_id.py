# This code pulls the data about restaurants from TripAdvisor.
# It takes as input list of Tripadvisor IDs, then scrapes data and saves it as a *.scv file.

from bs4 import BeautifulSoup
from selenium import webdriver
import time
import sys
import numpy as np
import pandas as pd
import re
import gc
import json
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By


column_list = ['id', 'actual_url', 'country_region', 'rest_name', 'is_claimed', 'rating', 'last_review', 'address',
               'latitude', 'longitude', 'popularity_top', 'popularity_detailed', 'price_range_and_top_tags',
               'n_reviews', 'travellers_choice', 'michelin', 'price_range', 'cuisines', 'meal_types', 'special_diets',
               'features', 'working_hours', 'telephone', 'website', 'food_rating', 'service_rating',
               'value_rating', 'atmosphere_rating', 'traveller_rating_5', 'traveller_rating_4',
               'traveller_rating_3', 'traveller_rating_2', 'traveller_rating_1', 'all_languages',
               'selected_language']

# Main function, that takes TripAdvisor restaurant ID and returns list of scraped features
def scrapeRestaurantInfo(restr_id):
    def check_exists_by_css_selector(css_selector_string):
        try:
            driver.find_element(By.CSS_SELECTOR, css_selector_string)
        except NoSuchElementException:
            return False
        return True

    def extract_bubble_rating(rating_type):
        if (soup.find("span", string=rating_type)) and (soup.find('div', {"class": "DzMcu"})):
            rating_area = soup.find("span", string=rating_type).parent#.parent
            if rating_area.find('span', {"class": "ui_bubble_rating"}):
                return rating_area.find('span', {"class": "ui_bubble_rating"})['class'][1]
            else:
                return 'None'
        else:
            return 'None'

    def extract_number_rating(rating_number):
        if soup.find('div', {"class": "ui_checkbox item", "data-tracker": rating_number}):
            return soup.find('div', {"class": "ui_checkbox item", "data-tracker": rating_number}).\
                find('span', {"class": "row_num"}).text
        else:
            return 0

    def extract_middle_column_feature(feature_name):
        if soup.find("div", string=feature_name):
            middle_column_feature = soup.find("div", string=feature_name).parent
            if middle_column_feature.find('div', {"class": "SrqKb"}):
                return middle_column_feature.find('div', {"class": "SrqKb"}).text
            else:
                return middle_column_feature.find('div', {"class": "AGRBq"}).text
        else:
            return 'None'

    # Create the url and load the webpage
    start_string = "https://www.tripadvisor.com/Restaurant_Review-"
    restr_url = start_string + restr_id
    #options = webdriver.chrome.options.Options()
    #options.add_argument("--headless")
    #driver = webdriver.Chrome(options=options)
    driver = webdriver.Chrome()
    driver.get(restr_url)

    # Make a list to store properties
    properties = []
    # Id used to generate url
    properties.append(restr_id)
    # Destination URL
    redirect_url = [driver.current_url]
    properties.append(redirect_url)

    # Check if there was a redirect
    if start_string not in driver.current_url:
        driver.close()
        return properties

    # Press the button to show number of reviews in each language
    if check_exists_by_css_selector('.item[data-value="ALL"]')\
            & (check_exists_by_css_selector('.item[data-value="ALL"] input[checked="checked"]') is False):
        all_lang_button = driver.find_element(By.CSS_SELECTOR, '.item[data-value="ALL"] input')
        all_lang_button.click()
        time.sleep(3)

    soup = BeautifulSoup(driver.page_source, features="lxml")
    #country and region
    breadcrumb = soup.find_all('li', {"class": "breadcrumb"})
    country_region_list = []
    for element in breadcrumb:
        country_region_list.append(element.text.strip())
    properties.append(country_region_list)
    #restraunt name
    properties.append(soup.find('h1', {"class": "HjBfq"}).text)
    #if restraunt is claimed
    properties.append(soup.find("div", {"class": "DkEDW"}).text)
    #average rating
    if soup.find('span', {"class": "ZDEqb"}):
        properties.append(soup.find('span', {"class": "ZDEqb"}).text.strip())
    else:
        properties.append('None')
    # last review
    if soup.find('span', {"class": "ratingDate"}):
        properties.append(soup.find('span', {"class": "ratingDate"})['title'])
    else:
        properties.append('None')
    #address
    properties.append(soup.find_all('a', {"class": "AYHFM"})[1].text.strip())
    #latitude
    if re.findall('latitude":"(.*)","longitude', driver.page_source):
        properties.append(re.findall('latitude":"(.*)","longitude', driver.page_source)[0])
    else:
        properties.append('None')
    #longitude
    if re.findall('longitude":"(.*)","num_reviews', driver.page_source):
        properties.append(re.findall('longitude":"(.*)","num_reviews', driver.page_source)[0])
    else:
        properties.append('None')
    # popularity_top
    if soup.find_all('a', {"class": "AYHFM"}):
        properties.append(soup.find_all('a', {"class": "AYHFM"})[0].text)
    else:
        properties.append('None')
    #popularity_detailed
    if soup.find_all('div', {"class": "cNFlb"}):
        properties.append(soup.find_all('div', {"class": "cNFlb"})[0].text)
    else:
        properties.append('None')
    # top_price_range and top_keywords
    if soup.find_all('a', {"class": "dlMOJ"}):
        top_tag_names = []
        for i in range(len(soup.find_all('a', {"class": "dlMOJ"}))):
            top_tag_names.append(soup.find_all('a', {"class": "dlMOJ"})[i].text)
        properties.append(top_tag_names)
    else:
        properties.append('None')
    # number of reviews
    if soup.find('span', {"class": "reviews_header_count"}):
        properties.append(soup.find('span', {"class": "reviews_header_count"}).text.strip().split()[0])
    else:
        properties.append('None')
    # travellers choice
    if soup.find('div', {"class": "ZxCVv"}):
        properties.append(soup.find('div', {"class": "ZxCVv"}).text)
    else:
        properties.append('None')
    # michelin
    if soup.find('div', {"class": "VjUBU"}):
        properties.append(soup.find('div', {"class": "VjUBU"}).text)
    else:
        properties.append('None')
    #desc_price_range
    properties.append(extract_middle_column_feature('PRICE RANGE'))
    #cuisines
    properties.append(extract_middle_column_feature('CUISINES'))
    #meal_types
    if extract_middle_column_feature('Meals') != 'None':
        properties.append(extract_middle_column_feature('Meals'))
    else:
        meals_re = re.findall(',"meals":\{"tagCategoryId":233,"tags":(.*)},"features":\{"tagCategoryId',
                              driver.page_source)
        if len(meals_re) > 0:
            json_data = json.loads(meals_re[0])
            meals = []
            for tag in json_data:
                meals.append(tag['tagValue'])
            properties.append(meals)
        else:
            properties.append('None')
    #special diets
    properties.append(extract_middle_column_feature('Special Diets'))
    #features
    if extract_middle_column_feature('FEATURES') != 'None':
        properties.append(extract_middle_column_feature('FEATURES'))
    else:
        features_re = re.findall(',"features":{"tagCategoryId(.*)]},"establishmentType":', driver.page_source)
        if len(features_re) > 0:
            features_string = features_re[0] + ']},"establishmentType":'
            json_data = json.loads(re.findall('"tags"\:(.*)\}\,"establishmentType', features_string)[0])
            features = []
            for tag in json_data:
                features.append(tag['tagValue'])
            properties.append(features)
        else:
            properties.append('None')
    #working hours
    if soup.find("div", {'class': 'zuYLj'}):
        properties.append(soup.find("div", {'class': 'zuYLj'}).text)
    elif soup.find("span", {'data-automation': 'top-info-hours'}):
        properties.append(soup.find("span", {'data-automation': 'top-info-hours'}).text)
    else:
        properties.append('None')
    #telephone
    if soup.find("span", {"class": "phone"}):
        properties.append(soup.find("span", {"class": "phone"}).parent.parent['href'])
    else:
        properties.append('None')
    #website
    wide_string = re.findall('parent_display_name":"(.*)","address_obj', driver.page_source)
    if wide_string:
        if re.findall(',"website":"(.*)', wide_string[0]):
            properties.append(re.findall(',"website":"(.*)', wide_string[0])[0])
        else:
            properties.append('None')
    else:
        properties.append('None')
    #bubble ratings
    properties.append(extract_bubble_rating("Food"))
    properties.append(extract_bubble_rating("Service"))
    properties.append(extract_bubble_rating("Value"))
    properties.append(extract_bubble_rating("Atmosphere"))
    #traveller rating (number of reviews by rating)
    properties.append(extract_number_rating('5'))
    properties.append(extract_number_rating('4'))
    properties.append(extract_number_rating('3'))
    properties.append(extract_number_rating('2'))
    properties.append(extract_number_rating('1'))
    #data from all languages
    if soup.find('div', {"class": "prw_filters_detail_language"}):
        languages = soup.find('div', {"class": "prw_filters_detail_language"}).find_all('div', {"class": "item"})
        lang_names = []
        for lang in languages:
            lang_names.append(lang.text)
        properties.append(set(lang_names))
    else:
        properties.append('None')
    #selected language
    if soup.find('div', {"class": "prw_filters_detail_language"}):
        properties.append(soup.find('div', {"class": "prw_filters_detail_language"}).find('input', {"checked": "checked"})['value'])
    else:
        properties.append('None')
    driver.close()
    return properties

def scrape_id_list(id_list, save_path):
    df = pd.DataFrame(columns=column_list)
    for i, id_i in enumerate(id_list):
        try:
            scrape_list = scrapeRestaurantInfo(id_i)
            if len(scrape_list) < 10:
                scrape_list_new = ['None'] * len(column_list)
                for i in range(len(scrape_list)):
                    scrape_list_new[i] = scrape_list[i]
                scrape_list = scrape_list_new
            df = df._append(pd.DataFrame([scrape_list], columns=column_list), ignore_index=True)
            print(scrape_list[0])
        except Exception as e:
            print("https://www.tripadvisor.com/Restaurant_Review-" + id_i)
            print(e)
        df.to_csv(save_path, index=False)
        time.sleep(10)


# Code to use when testing in python console
"""
def check_exists_by_css_selector(css_selector_string):
    try:
        driver.find_element(By.CSS_SELECTOR, css_selector_string)
    except NoSuchElementException:
        return False
    return True

#https://www.tripadvisor.com/Restaurant_Review-g1024119-d2320962
driver = webdriver.Chrome()
driver.get(restr_url)
soup = BeautifulSoup(driver.page_source, features="lxml")

id_list = ["g186470-d8838644", "g186470-d8863349", "g186470-d9697176", "g186470-d9778284", "g186470-d9849048"]
"""

# Code to find not scanned ids
#df = df.loc[df['selected_language'] != 'en']

#df_old = pd.read_csv('tripadvisor_european_restaurants.csv')
#df_old = df_old.loc[df_old['country'] == 'Northern Ireland']
#gc.collect()

#id_old = df_old['restaurant_link'].reset_index()
#id_new = df['id'].reset_index(drop=True)
#ids = id_old.merge(id_new, left_on='restaurant_link', right_on='id', how='outer')
#id_list = list(ids.loc[ids['id'].isnull(), 'restaurant_link'])

if __name__ == '__main__':
    csv_path = sys.argv[1]
    country = sys.argv[2]
    position = int(sys.argv[3])
    output_path = sys.argv[4]

    df_old = pd.read_csv(csv_path)
    df_old = df_old.loc[df_old['country'] == country]
    gc.collect()
    id_list = df_old['restaurant_link'].iloc[position:]
    scrape_id_list(id_list, output_path)

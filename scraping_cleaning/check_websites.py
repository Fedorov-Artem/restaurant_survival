# Checks if website exists.
# If a website is a link to a Facebook account, it scrapes and saves account description and the last post.

from selenium import webdriver
import time
import sys

import numpy as np
import pandas as pd
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from urllib.parse import urlsplit

# Takes the url, scrapes it and returns the data
def scrapeWebsiteData(restr_url):
    # Scrapes a Facebook URL.
    def get_last_facebook_post(restr_url):
        def check_exists_by_css_selector(css_selector_string, sel_location=None):
            try:
                if sel_location is None:
                    driver.find_element(By.CSS_SELECTOR, css_selector_string)
                else:
                    sel_location.find_element(By.CSS_SELECTOR, css_selector_string)
            except NoSuchElementException:
                return False
            return True

        options = webdriver.chrome.options.Options()
        options.add_argument("--headless")
        driver = webdriver.Chrome(options=options)
        driver.get(restr_url)
        time.sleep(5)

        if check_exists_by_css_selector('[aria-label="Close"]'):
            close_button = driver.find_element(By.CSS_SELECTOR, '[aria-label="Close"]')
            close_button.click()
            time.sleep(7)

        if check_exists_by_css_selector('._585n'):
            driver.close()
            facebook_data = ['account_doesnt_exist', '', '', '', '', '']
            print(facebook_data)
            time.sleep(61)
            return facebook_data

        if check_exists_by_css_selector('._4-dp'):
            driver.close()
            facebook_data = ['account_not_found', '', '', '', '', '']
            time.sleep(61)
            return facebook_data

        if check_exists_by_css_selector('[src="/images/comet/empty_states_icons/permissions/permissions_gray_wash.svg"]'):
            driver.close()
            facebook_data = ['account_deleted', '', '', '', '', '']
            print(facebook_data)
            time.sleep(61)
            return facebook_data

        facebook_data = []

        if check_exists_by_css_selector('[role="article"]'):
            last_article = driver.find_element(By.CSS_SELECTOR, '[role="article"]')
            facebook_data.append('account_exists')
            facebook_data.append(last_article.find_element(By.CSS_SELECTOR, 'h2').text)
            if check_exists_by_css_selector('a.xo1l8bm[aria-label]', last_article):
                facebook_data.append(last_article.find_element(By.CSS_SELECTOR, 'a.xo1l8bm[aria-label]').text)
            elif check_exists_by_css_selector('a.xo1l8bm', last_article):
                facebook_data.append(last_article.find_element(By.CSS_SELECTOR, 'a.xo1l8bm').text)
            else:
                facebook_data.append('')
            if check_exists_by_css_selector('[data-ad-comet-preview="message"]', last_article):
                facebook_data.append(last_article.find_element(By.CSS_SELECTOR, '[data-ad-comet-preview="message"]').text)
            else:
                facebook_data.append('')
        else:
            facebook_data.append('account_exists')
            if check_exists_by_css_selector('h1'):
                facebook_data.append(driver.find_element(By.CSS_SELECTOR, 'h1').text)
            else:
                facebook_data.append('no_company_name')
            facebook_data.append('no_posts')
            facebook_data.append('no_posts')

        if check_exists_by_css_selector('.x1cy8zhl.xyamay9'):
            facebook_data.append(driver.find_element(By.CSS_SELECTOR, '.x1cy8zhl.xyamay9').text)
        elif check_exists_by_css_selector('.x193iq5w.xvq8zen.xo1l8bm.xi81zsa'):
            facebook_data.append(driver.find_element(By.CSS_SELECTOR, '.x193iq5w.xvq8zen.xo1l8bm.xi81zsa').text)
        else:
            facebook_data.append('')


        if check_exists_by_css_selector('.x1yztbdb'):
            facebook_data.append(driver.find_element(By.CSS_SELECTOR, '.x1yztbdb').text)
        else:
            facebook_data.append('')
        driver.close()
        time.sleep(61)
        return facebook_data

    # Checks is a site exists (in case if a site is not a Facebook account)
    def check_existance(restr_url):
        options = webdriver.chrome.options.Options()
        options.add_argument("--headless")
        driver = webdriver.Chrome(options=options)
        site_data = []
        try:
            driver.get(restr_url)
            if driver.title == '':
                all_text = driver.find_element(By.XPATH, "/html/body").text
                all_text = all_text[0:100]
                site_data.append(all_text)
            else:
                site_data.append(driver.title)
        except Exception as e:
            site_data.append('failed_to_access')

        time.sleep(4)
        home_url = "{0.scheme}://{0.netloc}/".format(urlsplit(restr_url))
        if home_url != restr_url:
            try:
                driver.get(home_url)
                if driver.title == '':
                    all_text = driver.find_element(By.XPATH, "/html/body").text
                    all_text = all_text[0:100]
                    site_data.append(all_text)
                else:
                    site_data.append(driver.title)
            except Exception as e:
                site_data.append('failed_to_access')
        else:
            site_data.append('')

        site_data.append('')
        site_data.append('')
        site_data.append('')
        site_data.append('')
        driver.close()
        return site_data

    # Clean the URL and call the function for Facebook or for non_facebook URLS
    if ('.facebook.' in restr_url) or ('/facebook.' in restr_url):
        if '://facebook.' in restr_url:
            restr_url = restr_url.replace('://facebook.', '://www.facebook.')

        # Remove prefix
        prefix_list = ['m.facebook.', 'en-gb.facebook.', 'sk-sk.facebook.', 'hu-hu.facebook.', 'cs-cz.facebook.',
                       'de-de.facebook.', 'bg-bg.facebook.', 'ru-ru.facebook.', 'ja-jp.facebook.', 'fi-fi.facebook.',
                       'web.facebook.']
        for prefix in prefix_list:
            if prefix in restr_url:
                restr_url = restr_url.replace(prefix, 'www.facebook.')

        if '.facebook.fi' in restr_url:
            restr_url = restr_url.replace('facebook.fi', 'facebook.com')
        if '/pg/' in restr_url:
            restr_url = restr_url.replace('/pg', '')

        # Remove suffix
        suffix_list = ['about/', 'menu/', 'info/', 'community/', 'timeline/', 'reviews/']
        for suffix in suffix_list:
            if ('/' + suffix) in restr_url:
                restr_url = restr_url.split(suffix)[0]
        try:
            url_data = get_last_facebook_post(restr_url)
        except Exception as e:
            print(restr_url + '  Error!!')
            url_data = ['error', '', '', '', '', '']
    else:
        if ('/en/' in restr_url) & ('raflaamo' in restr_url):
            restr_url = restr_url.replace('/en/', '/fi/')
        url_data = check_existance(restr_url)

    return url_data


column_list = ['id', 'website', 'is_available', 'homesite_user_name', 'last_update', 'facebook_text', 'subscribers',
               'description']

def scrape_list(df_urls, save_path):
    df_result = pd.DataFrame(columns=column_list)
    for i in range(len(df_urls)):
        check_results = []
        check_results.append(df_urls['id'].iloc[i])
        url = df_urls['website'].iloc[i]
        check_results.append(url)
        if len(str(url)) > 3:
            check_results = check_results + scrapeWebsiteData(url)
        else:
            check_results = check_results + ['', '', '', '', '', '']

        print(check_results)
        df_result = df_result._append(pd.DataFrame([check_results], columns=column_list), ignore_index=True)
        df_result.to_csv(save_path, index=False)

'''
df_result = pd.DataFrame(columns=column_list)

for i in range(4188,4500):
    check_results = []
    check_results.append(df['id'].iloc[i])
    url = df['website'].iloc[i]
    check_results.append(url)
    if len(str(url)) > 3:
        check_results = check_results + scrapeWebsiteData(url)
    else:
        check_results = check_results + ['', '', '', '', '', '']
    df_result = df_result._append(pd.DataFrame([check_results], columns=column_list), ignore_index=True)
    df_result.to_csv('FI_webscan.csv', index=False)
'''

# This code was used to join multiple files with scraping results, including those with error that were
# re-scraped several times. And then the data was combined with initial dataset to get one dataset.
'''
df_result = pd.concat([df_result, df_recheck])
df_result = df_result.drop_duplicates()
df_result = df_result.drop_duplicates('id', keep='last')

df = df.merge(df_result, on='id', how='outer')
#del df['is_available'], df['homesite_user_name'], df['last_update'], df['facebook_text'], df['subscribers'], df['description']
del df['website_x']
df = df.rename(columns={"website_y": "website"})

df.to_csv('FI_webscan_all_columns_raw.csv', index=False)
'''

if __name__ == '__main__':
    csv_path = sys.argv[1]
    position = int(sys.argv[2])
    output_path = sys.argv[3]

    df_urls = pd.read_csv(csv_path)
    df_urls = df_urls.iloc[position:]
    scrape_list(df_urls, output_path)
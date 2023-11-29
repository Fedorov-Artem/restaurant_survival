# Ceate a list of all cities with restaurants in a country on TripAdvisor

from selenium import webdriver
import time

import numpy as np
import pandas as pd
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

city_urls_ni =[
    'https://www.tripadvisor.com/Restaurants-g186470-Belfast_Northern_Ireland.html',
    'https://www.tripadvisor.com/Restaurants-g186482-Derry_County_Londonderry_Northern_Ireland.html',
    'https://www.tripadvisor.com/Restaurants-g191277-Bangor_County_Down_Northern_Ireland.html',
    'https://www.tripadvisor.com/Restaurants-g209938-Newry_County_Down_Northern_Ireland.html',
    'https://www.tripadvisor.com/Restaurants-g445040-Lisburn_County_Antrim_Northern_Ireland.html',
    'https://www.tripadvisor.com/Restaurants-g551726-Ballymena_County_Antrim_Northern_Ireland.html',
    'https://www.tripadvisor.com/Restaurants-g209950-Newtownabbey_County_Antrim_Northern_Ireland.html',
    'https://www.tripadvisor.com/Restaurants-g209956-Coleraine_County_Londonderry_Northern_Ireland.html',
    'https://www.tripadvisor.com/Restaurants-g190795-Enniskillen_County_Fermanagh_Northern_Ireland.html',
    'https://www.tripadvisor.com/Restaurants-g209953-Newtownards_County_Down_Northern_Ireland.html',
    'https://www.tripadvisor.com/Restaurants-g209955-Banbridge_County_Down_Northern_Ireland.html',
    'https://www.tripadvisor.com/Restaurants-g209947-Carrickfergus_County_Antrim_Northern_Ireland.html',
    'https://www.tripadvisor.com/Restaurants-g209952-Portrush_County_Antrim_Northern_Ireland.html',
    'https://www.tripadvisor.com/Restaurants-g186474-Armagh_County_Armagh_Northern_Ireland.html',
    'https://www.tripadvisor.com/Restaurants-g635930-Magherafelt_County_Londonderry_Northern_Ireland.html',
    'https://www.tripadvisor.com/Restaurants-g186484-Omagh_County_Tyrone_Northern_Ireland.html',
    'https://www.tripadvisor.com/Restaurants-g635686-Antrim_County_Antrim_Northern_Ireland.html',
    'https://www.tripadvisor.com/Restaurants-g186478-Newcastle_County_Down_Northern_Ireland.html',
    'https://www.tripadvisor.com/Restaurants-g209972-Craigavon_County_Armagh_Northern_Ireland.html',
    'https://www.tripadvisor.com/Restaurants-g209959-Portadown_County_Armagh_Northern_Ireland.html'
]

city_urls_sk =[
    'https://www.tripadvisor.com/Restaurants-g274924-Bratislava_Bratislava_Region.html',
    'https://www.tripadvisor.com/Restaurants-g274927-Kosice_Kosice_Region.html',
    'https://www.tripadvisor.com/Restaurants-g274933-Nitra_Nitra_Region.html',
    'https://www.tripadvisor.com/Restaurants-g274946-Zilina_Zilina_Region.html',
    'https://www.tripadvisor.com/Restaurants-g799591-Presov_Presov_Region.html',
    'https://www.tripadvisor.com/Restaurants-g274923-Banska_Bystrica_Banska_Bystrica_Region.html',
    'https://www.tripadvisor.com/Restaurants-g663679-Trnava_Trnava_Region.html',
    'https://www.tripadvisor.com/Restaurants-g274945-Trencin_Trencin_Region.html',
    'https://www.tripadvisor.com/Restaurants-g274938-Poprad_Presov_Region.html',
    'https://www.tripadvisor.com/Restaurants-g274929-Liptovsky_Mikulas_Zilina_Region.html',
    'https://www.tripadvisor.com/Restaurants-g274935-Piestany_Trnava_Region.html',
    'https://www.tripadvisor.com/Restaurants-g274931-Martin_Zilina_Region.html',
    'https://www.tripadvisor.com/Restaurants-g799606-Zvolen_Banska_Bystrica_Region.html',
    'https://www.tripadvisor.com/Restaurants-g612451-Banska_Stiavnica_Banska_Bystrica_Region.html',
    'https://www.tripadvisor.com/Restaurants-g285717-Komarno_Nitra_Region.html',
    'https://www.tripadvisor.com/Restaurants-g2540356-Hlohovec_Trnava_Region.html',
    'https://www.tripadvisor.com/Restaurants-g274942-Spisska_Nova_Ves_Kosice_Region.html',
    'https://www.tripadvisor.com/Restaurants-g1077229-Pezinok_Bratislava_Region.html',
    'https://www.tripadvisor.com/Restaurants-g642204-Prievidza_Trencin_Region.html',
    'https://www.tripadvisor.com/Restaurants-g675047-Ruzomberok_Zilina_Region.html'
]

city_urls_bg =[
    'https://www.tripadvisor.com/Restaurants-g294452-Sofia_Sofia_Region.html',
    'https://www.tripadvisor.com/Restaurants-g295391-Plovdiv_Plovdiv_Province.html',
    'https://www.tripadvisor.com/Restaurants-g295392-Varna_Varna_Province.html',
    'https://www.tripadvisor.com/Restaurants-g499086-Sunny_Beach_Burgas_Province.html',
    'https://www.tripadvisor.com/Restaurants-g635766-Burgas_Burgas_Province.html',
    'https://www.tripadvisor.com/Restaurants-g303648-Nessebar_Burgas_Province.html',
    'https://www.tripadvisor.com/Restaurants-g318870-Bansko_Blagoevgrad_Province.html',
    'https://www.tripadvisor.com/Restaurants-g635769-Sozopol_Burgas_Province.html',
    'https://www.tripadvisor.com/Restaurants-g1088372-Sveti_Vlas_Burgas_Province.html',
    'https://www.tripadvisor.com/Restaurants-g608699-Ruse_Ruse_Province.html',
    'https://www.tripadvisor.com/Restaurants-g303653-Veliko_Tarnovo_Veliko_Tarnovo_Province.html',
    'https://www.tripadvisor.com/Restaurants-g303647-Borovets_Sofia_Region.html',
    'https://www.tripadvisor.com/Restaurants-g303646-Balchik_Dobrich_Province.html',
    'https://www.tripadvisor.com/Restaurants-g663130-Pomorie_Burgas_Province.html',
    'https://www.tripadvisor.com/Restaurants-g303651-Stara_Zagora_Stara_Zagora_Province.html',
    'https://www.tripadvisor.com/Restaurants-g499087-Golden_Sands_Varna_Province.html',
    'https://www.tripadvisor.com/Restaurants-g1157167-Sliven_Sliven_Province.html',
    'https://www.tripadvisor.com/Restaurants-g939861-Primorsko_Burgas_Province.html',
    'https://www.tripadvisor.com/Restaurants-g1788899-Lozenets_Burgas_Province.html',
    'https://www.tripadvisor.com/Restaurants-g1156161-Blagoevgrad_Blagoevgrad_Province.html'
]

city_urls_fi =[
    'https://www.tripadvisor.com/Restaurants-g189934-Helsinki_Uusimaa.html',
    'https://www.tripadvisor.com/Restaurants-g189948-Tampere_Pirkanmaa.html',
    'https://www.tripadvisor.com/Restaurants-g189949-Turku_Southwest_Finland.html',
    'https://www.tripadvisor.com/Restaurants-g189932-Espoo_Uusimaa.html',
    'https://www.tripadvisor.com/Restaurants-g226906-Vantaa_Uusimaa.html',
    'https://www.tripadvisor.com/Restaurants-g189929-Oulu_Northern_Ostrobothnia.html',
    'https://www.tripadvisor.com/Restaurants-g189942-Jyvaskyla_Central_Finland.html',
    'https://www.tripadvisor.com/Restaurants-g189937-Lahti_Tavastia_Proper.html',
    'https://www.tripadvisor.com/Restaurants-g227603-Lappeenranta_South_Karelia.html',
    'https://www.tripadvisor.com/Restaurants-g189908-Kuopio_Northern_Savonia.html',
    'https://www.tripadvisor.com/Restaurants-g784762-Kouvola_Kymenlaakso.html',
    'https://www.tripadvisor.com/Restaurants-g189945-Pori_Satakunta.html',
    'https://www.tripadvisor.com/Restaurants-g189922-Rovaniemi_Lapland.html',
    'https://www.tripadvisor.com/Restaurants-g189951-Vaasa_Ostrobothnia.html',
    'https://www.tripadvisor.com/Restaurants-g189905-Joensuu_North_Karelia.html',
    'https://www.tripadvisor.com/Restaurants-g262036-Hameenlinna_Tavastia_Proper.html',
    'https://www.tripadvisor.com/Restaurants-g189898-Aland_Island_Aland.html',
    'https://www.tripadvisor.com/Restaurants-g230040-Seinajoki_Southern_Ostrobothnia.html',
    'https://www.tripadvisor.com/Restaurants-g315777-Porvoo_Uusimaa.html',
    'https://www.tripadvisor.com/Restaurants-g189936-Kotka_Kymenlaakso.html'
]


def scrapeCitiesList(list_url):
    def check_exists_by_css_selector(css_selector_string):
        try:
            driver.find_element(By.CSS_SELECTOR, css_selector_string)
        except NoSuchElementException:
            return False
        return True

    options = webdriver.chrome.options.Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    #driver = webdriver.Chrome()
    driver.get(list_url)

    city_url_list = []

    city_list = driver.find_element(By.CLASS_NAME, "geoList")
    city_urls = city_list.find_elements(By.TAG_NAME, 'a')

    for city_url in city_urls:
        city_url_list.append(city_url.get_attribute("href"))

    return city_url_list

#url_list_i = scrapeCitiesList('https://www.tripadvisor.com/Restaurants-g186469-oa40-Northern_Ireland.html#LOCATION_LIST')
#city_urls = city_urls + url_list_i

i = 4
while i < 45:
    url_i = 'https://www.tripadvisor.com/Restaurants-g189896-oa' + str(i) + '0-Finland.html#LOCATION_LIST'
    url_list_i = scrapeCitiesList(url_i)
    city_urls = city_urls + url_list_i
    print(str(len(city_urls)))
    i = i + 2
    time.sleep(15)

df = pd.DataFrame(city_urls)
df.to_csv('NI_city_lists.csv')

#driver = webdriver.Chrome()
#driver.get(start_url)
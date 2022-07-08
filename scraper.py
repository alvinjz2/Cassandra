from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from heapq import heappush
from multiprocessing import Pool
import time
buy, sell = [], []
global_listings = []
def scrape_listing_sell(index):
    actions = global_listings[index].find_element(By.CLASS_NAME, 'listing__details__actions')
    if actions.text == 'BOT': # filter listings to only get bots
        price = tuple(global_listings[index].find_element(By.TAG_NAME, 'a').find_element(By.CLASS_NAME, 'item__price').text.split(' '))
        price = (float(price[0]) *-1, price[1]) 
        trade_offer = actions.find_element(By.TAG_NAME, 'a').get_attribute('href')
        order = (price, trade_offer)
        heappush(sell, order) 

def scrape_listing_buy(index):
    actions = global_listings[index].find_element(By.CLASS_NAME, 'listing__details__actions')
    if actions.text == 'BOT': # filter listings to only get bots
        price = tuple(global_listings[index].find_element(By.TAG_NAME, 'a').find_element(By.CLASS_NAME, 'item__price').text.split(' '))
        price = (float(price[0]), price[1])
        trade_offer = actions.find_element(By.TAG_NAME, 'a').get_attribute('href')
        order = (price, trade_offer)
        heappush(buy, order) 

def scrape_orders(ret, orders):
    listing = orders.find_elements(By.CLASS_NAME, 'listing')

def browse(link):
    s = time.perf_counter_ns()
    driver =  webdriver.Chrome(service=Service(executable_path=ChromeDriverManager().install()))
    driver.get(link)
    elem = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'col-lg-6')))
    orders = driver.find_elements(By.CLASS_NAME, 'col-lg-6')
    for i, o in enumerate(orders): # first set is buy, second is sell
        listings = o.find_elements(By.CLASS_NAME, 'listing')
        global_listings.extend(listings)
        with Pool() as pool:
            if not i:
                pool.map(scrape_listing_buy, range(0,4))
            else:
                pool.map(scrape_listing_sell, range(5,9))
    print(f'time elapsed: {time.perf_counter_ns() - s}')
    return buy, sell
    
def browse2(link):
    s = time.perf_counter_ns()
    driver =  webdriver.Chrome(service=Service(executable_path=ChromeDriverManager().install()))
    driver.get(link)
    elem = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'col-lg-6')))
    orders = driver.find_elements(By.CLASS_NAME, 'col-lg-6')
    buy, sell = [], []
    for i, o in enumerate(orders): # first set is buy, second is sell
        listings = o.find_elements(By.CLASS_NAME, 'listing')
        for j, listing in enumerate(listings):
            actions = listing.find_element(By.CLASS_NAME, 'listing__details__actions')
            if actions.text == 'BOT': # filter listings to only get bots
                price = tuple(listing.find_element(By.TAG_NAME, 'a').find_element(By.CLASS_NAME, 'item__price').text.split(' '))
                price = (float(price[0]) *-1, price[1]) if i else (float(price[0]), price[1])
                trade_offer = actions.find_element(By.TAG_NAME, 'a').get_attribute('href')
                order = (price, trade_offer)
                heappush(buy, order) if not i else heappush(sell, order)
    print(f'time elapsed: {time.perf_counter_ns() - s}')
    return buy, sell



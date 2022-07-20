from concurrent.futures import ThreadPoolExecutor
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from heapq import heappush

import time
import threading
buy, sell = [], []

def sub_worker(item, method, i):
    if method == "price":
        price = tuple(item.find_element(By.TAG_NAME, 'a').find_element(By.CLASS_NAME, 'item__price').text.split(' '))
        price = (float(price[0]) *-1, price[1]) if i else (float(price[0]), price[1])
        return price
    elif method == "actions":
        trade_offer = item.find_element(By.TAG_NAME, 'a').get_attribute('href')
        return trade_offer

def worker(listing, i):
    executor = ThreadPoolExecutor(max_workers=10)
    actions = listing.find_element(By.CLASS_NAME, 'listing__details__actions')
    if actions.text == 'BOT': # filter listings to only get bots
        future_price = executor.submit(sub_worker, listing, "price", i)
        future_trade_offer = executor.submit(sub_worker, actions, "actions", i)
        order = (future_price.result(), future_trade_offer.result())
        threading.Lock().acquire()
        heappush(buy, order) if not i else heappush(sell, order)
        threading.Lock().release()

def browse(link):
    s = time.perf_counter_ns()
    driver =  webdriver.Chrome(service=Service(executable_path=ChromeDriverManager().install()))
    driver.get(link)
    elem = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'col-lg-6')))
    orders = driver.find_elements(By.CLASS_NAME, 'col-lg-6')
    print(f'time elapsed to scrape initially: {time.perf_counter_ns() - s}')
    s = time.perf_counter_ns()
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
    
def browse2(link):
    s = time.perf_counter_ns()
    driver =  webdriver.Chrome(service=Service(executable_path=ChromeDriverManager().install()))
    driver.get(link)

    elem = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'col-lg-6')))
    orders = driver.find_elements(By.CLASS_NAME, 'col-lg-6')
    print(f'time elapsed to scrape initially: {time.perf_counter_ns() - s}')
    s = time.perf_counter_ns()
    executor = ThreadPoolExecutor(max_workers=10)
    for i, o in enumerate(orders): # first set is buy, second is sell
        listings = o.find_elements(By.CLASS_NAME, 'listing')
        for j, listing in enumerate(listings):
            executor.submit(worker, listing, i)
    executor.shutdown()
    print(f'time elapsed, multithreading: {time.perf_counter_ns() - s}')
    print(buy)
    print(sell)
    return buy, sell

key = 'https://next.backpack.tf/stats?item=Mann%20Co.%20Supply%20Crate%20Key&quality=Unique'
browse2(key)
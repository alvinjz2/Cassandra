from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager 
from selenium.webdriver.common.by import By
from heapq import heappush

link = "https://backpack.tf/stats/Unique/Mann%20Co.%20Supply%20Crate%20Key/Tradable/Craftable"
link2 = 'https://next.backpack.tf/stats?item=Mann%20Co.%20Supply%20Crate%20Key&quality=Unique'
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.implicitly_wait(5)

def browse(driver, link):
    driver.get(link)
    buy, sell = [], []
    orders = driver.find_elements(By.CLASS_NAME, 'col-lg-6')
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
    return buy, sell
    
browse(driver, link2)
driver.quit()



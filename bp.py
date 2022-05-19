import undetected_chromedriver.v2 as uc
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import re
driver = uc.Chrome(use_subprocess = True, suppress_welcome=False)
key = "43268E7C04682E63C853EE911BE21AD4"
link = 'https://backpack.tf/stats/Unique/Mann%20Co.%20Supply%20Crate%20Key/Tradable/Craftable'
link2 = 'https://next.backpack.tf/stats?item=Mann%20Co.%20Supply%20Crate%20Key&quality=Unique'
driver.get(link2) 
driver.implicitly_wait(15)
driver.quit()
orders = driver.find_elements(By.CLASS_NAME, 'media-list')

for i, o in enumerate(orders): # first set is buy, second is sell
    print(f'Sell Orders') if not i else print(f'Buy Orders')
    listings = o.find_elements(By.CLASS_NAME, 'listing')
    for j, listing in enumerate(listings):
        item_details = listing.find_element(By.CLASS_NAME, 'listing-item')
        item = item_details.get_attribute('innerHTML')
        task=re.search('var task = (.*);',item)
        button = listing.find_element(By.CLASS_NAME, 'listing-buttons').find_element(By.CSS_SELECTOR, 'a')
        text = button.get_attribute('outerHTML')
        trade_offer_url = button.get_attribute('href')
        if 'managed by a user agent' in text:
            print(f'Listing {j}: {item_details.text} \n{trade_offer_url}')
            #print(item_details.text)



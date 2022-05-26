from scraper import browse
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager 
from selenium.webdriver.chrome.service import Service

class Asset:
    def __init__(self, link):
        self.link = link
        self.bid, self.ask = None, None
        # have bid/ask lists, with tuples of the form (price, trade_url) in a priority queue. bid is decreasing, ask is increasing
        
    def update(self):
        res = browse(self.link)
        self.bid, self.ask = res[1], res[0]

    def opportunity(self):
        if abs(self.bid[0][0][0]) > abs(self.ask[0][0][0]):
            print(f'Bid: {self.bid[0]}. Ask: {self.ask[0]}. \n Arbitrage possible.')
            return True
        print('No arbitrage present.')
        return False

    def arbitrage(self):
        if self.opportunity:
            return True

link = 'https://next.backpack.tf/stats?item=Mann%20Co.%20Supply%20Crate%20Key&quality=Unique'

a = Asset(link)
a.update()
a.opportunity()
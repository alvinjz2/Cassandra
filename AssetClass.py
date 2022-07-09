from Scraper import browse
from utils import partner_to_64id
import asyncio

class AssetClass:
    def __init__(self, link):
        self.link = link
        self.asks, self.bids = browse(self.link)
        
    def update(self):
        res = browse(self.link)
        self.bids, self.asks = res[1], res[0]

    def opportunity(self):
        self.update()
        bid, ask = abs(self.bids[0][0][0]), abs(self.asks[0][0][0])
        ret = [False, bid, ask, self.bids[0][0][1], self.asks[0][0][1],
                     self.bids[0][1], self.asks[0][1], partner_to_64id(self.bids[0][1]), partner_to_64id(self.asks[0][1])]
        if bid > ask:
           ret[0] = True
        return tuple(ret)

    def worker(self):
        return None

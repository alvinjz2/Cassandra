from scraper import browse
from utils import partner_to_64id
class Asset:
    def __init__(self, link):
        self.link = link
        self.bids, self.asks = None, None
        
    def update(self):
        res = browse(self.link)
        self.bids, self.asks = res[1], res[0]

    def opportunity(self):
        self.update()
        bid, ask = abs(self.bids[0][0][0]), abs(self.asks[0][0][0])
        bid_offer, ask_offer =  self.bids[0][1], self.asks[0][1]
        bid_t, ask_t = self.bids[0][0][1], self.asks[0][0][1]
        bid_id, ask_id = partner_to_64id(bid_offer), partner_to_64id(ask_offer)
        if bid > ask:
            return (True, bid, ask, bid_t, ask_t, bid_offer, ask_offer, bid_id, ask_id)
        return (False, bid, ask, bid_t, ask_t, bid_offer, ask_offer, bid_id, ask_id)

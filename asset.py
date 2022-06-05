from scraper import browse

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
        if bid > ask:
            print(f'Bid: {bid}. Ask: {ask}. \n Arbitrage possible.')
            return True
        print(f'Bid: {bid}. Ask: {ask}. \n No arbitrage possible.')
        return False

    def arbitrage(self):
        if self.opportunity:
            # execute trade
            return True

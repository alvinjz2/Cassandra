from scraper import browse

class Asset:
    def __init__(self, link):
        self.link = link
        self.bid, self.ask = None, None
        # have bid/ask lists, with tuples of the form (price, trade_url) in a priority queue. bid is decreasing, ask is increasing
        
    def update(self):
        res = browse(self.link)
        self.bid, self.ask = res[1], res[0]

    def opportunity(self):
        if abs(self.bid[0][0][0]) > abs(self.ask[0][0][0]): # compare value
            print(f'Bid: {self.bid[0]}. Ask: {self.ask[0]}. \n Arbitrage possible.')
            return True
        print(f'Bid: {self.bid[0]}. Ask: {self.ask[0]}. \n No arbitrage possible.')
        return False

    def arbitrage(self):
        if self.opportunity:
            # execute trade
            return True

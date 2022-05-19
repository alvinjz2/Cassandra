from scraper import browse
class Asset:
    def __init__(self, link, driver):
        self.link = link
        self.driver = driver
        self.bid, self.ask = None, None
        # have bid/ask lists, with tuples of the form (price, trade_url) in a priority queue. bid is decreasing, ask is increasing
    def update(self, link, driver):
        self.bid, self.ask = browse(self.driver, self.link)[1], browse(self.driver, self.link)[0]

    def opportunity(self):
        if self.bid[0] > self.ask[0]:
            return True
        return False

    def arbitrage(self):
        if self.opportunity:
            return True
from steampy.client import SteamClient
from utils import pure_balance, partner_to_64id, find_tf2item, get_tf2capital, resize_offer
from heapq import heappop
import time
import asyncio

class Bot:
    def __init__(self, username, password, api_key, steamguard, game):
        self.client = SteamClient(api_key)
        try:
            self.client.login(username, password, steamguard)
            print('Logged in')
        except:
            print(f'Could not login')
        self.steam_id = self.client.steam_guard['steamid']
        self.game = game
        self.capital = get_tf2capital(self.steam_id)
        self.balance = pure_balance(len(self.capital['metals']['ref']), len(self.capital['metals']['rec']), len(self.capital['metals']['scrap']))
        self.tasks = asyncio.Queue()

    def trade_buy(self, quantity, item, price, partner_url):
        start, end = time.time(), None
        own = resize_offer(self.capital, price)
        partner = find_tf2item(partner_to_64id(partner_url), quantity, item)
        if not partner or not own:
            print('Insuffient funds')
            return False
        try:
            offer = self.client.make_offer_with_url(items_from_me=own, items_from_them=partner, trade_offer_url=partner_url, case_sensitive=True)
            end = time.time()
            print(offer)
            return end - start
        except:
            return None


    def trade_sell(self, quantity, item, price, partner_url):
        start, end = time.time(), None
        own = find_tf2item(self.steam_id, quantity, item)
        partner = resize_offer(get_tf2capital(partner_to_64id(partner_url)), price)
        if not partner or not own:
            print('Insuffient funds')
            return False
        try:
            offer = self.client.make_offer_with_url(items_from_me=own, items_from_them=partner, trade_offer_url=partner_url, case_sensitive=True)
            end = time.time()
            print(offer)
            return end - start
        except:
            return None

    
    def arbitrage(self, asset):
        max_wait = 5000
        bid, ask = abs(asset.bids[0][0][0]), abs(asset.asks[0][0][0])
        buyer_url, seller_url = self.bids[0][1], self.asks[0][1]
        while bid > ask:
            buy_offer = self.trade_buy(1, 'key', ask, seller_url)[0]
            if not buy_offer:
                print(f'Didn\'t buy item.')
                asset.asks.heappop()
                ask, seller_url =  abs(asset.asks[0][0][0]), self.asks[0][1]
                continue
            s = time.process_time_ns()
            while self.client.get_trade_offers_summary()['response']['newly_accepted_sent_count'] == 0:
                t1 = time.process_time_ns() - s
                if t1 > max_wait:
                    print('Took too long, abandon buy trade')
                    asset.asks.heappop()
                    ask, seller_url =  abs(asset.asks[0][0][0]), self.asks[0][1]
                    continue
            sell_offer = self.trade_sell(1, 'key', bid, buyer_url)[0]
            if not sell_offer:
                print(f'Didn\'t sell item.')
                asset.bids.heappop()
                bid, buyer_url =  abs(asset.bids[0][0][0]), self.bids[0][1]
                continue
            s = time.process_time_ns()
            while self.client.get_trade_offers_summary()['newly_accepted_sent_count'] == 0:
                t2 = time.process_time_ns() - s
                if t2 > max_wait:
                    print(f'Didn\'t sell item.')
                    asset.bids.heappop()
                    bid, buyer_url =  abs(asset.bids[0][0][0]), self.bids[0][1]
                    continue
            print(buy_offer['success'] and sell_offer['success'])

    
    def worker(self, name):
        return None





       




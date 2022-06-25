from steampy.client import SteamClient
from utils import pure_balance, partner_to_64id, find_tf2item, get_tf2capital, resize_offer
from heapq import heappop
import time
import asyncio
import datetime

#all bots use the same script, maybe add them and type command
# need to keep more scrap on hand to not miss any trade offers.
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


    def buy_from(self, price):
        start, end = time.process_time_ns(), None
        buy_from =  resize_offer(self.capital, price)      
        end = time.process_time_ns() - start
        if buy_from:
            return end, buy_from
        if not buy_from:
            print(f'Couldn\'t buy the item priced at {price}.')
            return False


    def sell_to(self, quantity, item):
        start, end = time.process_time_ns(), None  
        sell_to = find_tf2item(self.steam_id, quantity, item)
        end = time.process_time_ns() - start
        if sell_to:
            return end, sell_to
        if not sell_to:
            print(f'Could not sell {quantity} of {item}.')
        return False


    def crosscheck(self, seller_url, buyer_url, quantity, item, buy_price):
        start, end = time.process_time_ns(), None
        seller = find_tf2item(partner_to_64id(seller_url), quantity, item)
        buyer = resize_offer(get_tf2capital(partner_to_64id(buyer_url)), buy_price)
        end = time.process_time_ns() - start
        if seller and buyer:
            return end, seller, buyer
        if not seller:
            return 'Seller Issue', seller_url
        if not buyer:
            return 'Buyer Issue', buyer_url


    def execute_trade(self, own, partner, url):
        try:
            offer = self.client.make_offer_with_url(items_from_me=own, items_from_them=partner, trade_offer_url=url, case_sensitive=True)
            return (True, offer)
        except:
            return False
    
    
    def arbitrage(self, asset):
        max_wait = 15
        buy_accepted, sell_accepted = False, False
        while (len(asset.bids) > 0 and len(asset.asks) > 0) and abs(asset.bids[0][0][0]) > abs(asset.asks[0][0][0]):
            check = self.crosscheck(asset.asks[0][1], asset.bids[0][1], 1, 'key', abs(asset.bids[0][0][0]))
            print(f'seller url:{asset.asks[0][1]}, buyer url:{asset.bids[0][1]}, 1, key, buy price:{abs(asset.bids[0][0][0])}')
            buy_amount = self.buy_from(abs(asset.asks[0][0][0]))
            if not buy_amount:
                print(heappop(asset.asks))
                continue
            if check[0] == 'Buyer Issue':
                print(f'Buyer issue, {check[1]} not enough pure')
                try:
                    print(heappop(asset.bids))
                except IndexError:
                    raise IndexError
            if check[0] == 'Seller Issue':
                print(f'Seller issue, {check[1]} did not have the item')
                try:
                    print(heappop(asset.asks))
                except IndexError:
                    raise IndexError
            if check[0] == 'Buyer Issue' or check[0] == 'Seller Issue':
                print('Not attempting')
                continue
            s = time.perf_counter_ns()
            buy_order = self.execute_trade(buy_amount[1], check[1], asset.asks[0][1])
            print(f'sent offer at {datetime.datetime.now()}')
            e = time.perf_counter_ns()
            print(f'time to process: {check[0] + (e-s)}')
            s = time.time()
            
            while self.client.get_trade_offers_summary()['response']['newly_accepted_sent_count'] == 0 and time.time() - s < max_wait:
                if self.client.get_trade_offers_summary()['response']['newly_accepted_sent_count'] > 0:
                    buy_accepted = True
                    break
                time.sleep(0.1)
            if buy_accepted:
                print(f'Purchased item')
            if not buy_accepted:
                print(f'Max time exceeded')
                heappop(asset.asks)
                try:
                    self.client.cancel_trade_offer(buy_order[1]['tradeofferid'])
                    print(f'canceled offer at {datetime.datetime.now()}')
                except:
                    print(f'Couldn\'t cancel trade offer, likely due to offer not existing')
                continue
            while buy_accepted and not sell_accepted:
                if (len(asset.bids) > 0 and len(asset.asks) > 0) and abs(asset.bids[0][0][0]) > abs(asset.asks[0][0][0]):
                    check = self.crosscheck(asset.asks[0][1], asset.bids[0][1], 1, 'key', abs(asset.bids[0][0][0]))
                    sell_to = self.sell_to(1, 'key')
                    sell_order = self.execute_trade(sell_to[1], check[2], asset.bids[0][1])
                    s = time.perf_counter_ns()
                    while time.perf_counter_ns() - s < max_wait:
                        if self.client.get_trade_offers_summary()['response']['newly_accepted_sent_count'] > 0:
                            sell_accepted = True
                            break
                    if not sell_accepted:
                        heappop(asset.asks)
                        try:
                            self.client.cancel_trade_offer(sell_order[1]['tradeofferid'])
                        except:
                            print(f'Couldn\'t cancel trade offer')
                            continue
                else:
                    print(f'Bought key but no arbitrage')
                    return
            if buy_accepted and sell_accepted:
                print(f'Arbitraged')
            else:
                print(f'No arbitrage at all')
            

    def worker(self, name):
        return None





       




from steampy.client import SteamClient
from utils import pure_balance, partner_to_64id, find_tf2item, get_tf2capital, resize_offer
import time

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


    def trade_buy(self, quantity, item, price, partner_url):
        partner = find_tf2item(partner_to_64id(partner_url), quantity, item)
        own = resize_offer(self.capital, price)
        if not partner or not own:
            print('Insuffient funds')
            return
        try:
            offer = self.client.make_offer_with_url(items_from_me=own, items_from_them=partner, trade_offer_url=partner_url, 
                                                    case_sensitive=True, message='Test sending trade offers')
            print(offer)
            return offer
        except:
            return None


    def trade_sell(self, quantity, item, price, partner_url):
        own = find_tf2item(self.steam_id, quantity, item)
        partner = resize_offer(get_tf2capital(partner_to_64id(partner_url)), price)
        if not partner or not own:
            print('Insuffient funds')
            return
        try:
            offer = self.client.make_offer_with_url(items_from_me=own, items_from_them=partner, trade_offer_url=partner_url, 
                                                    case_sensitive=True, message='Test sending trade offers')
            print(offer)
            return offer
        except:
            return None

    
    def arbitrage(self, asset):
        return None
       




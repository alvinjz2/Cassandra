from ctypes import resize
from steampy.client import SteamClient, Asset
from utils import item_class_ids, pure_assets, resize_offer, pure_balance, partner_to_64id


class Bot:
    def __init__(self, username, password, api_key, steamguard, game):
        self.client = SteamClient(api_key)
        try:
            self.client.login(username, password, steamguard)
            print('Logged in')
        except Exception as e:
            print(f'Could not login.\n Error message: {e}')

        self.game = game
        self.steam_id = self.client.steam_guard['steamid']
        self.capital = self.get_capital(self.steam_id)
        self.balance = pure_balance(len(self.capital['metals']['ref']), len(self.capital['metals']['rec']), len(self.capital['metals']['scrap']))

    def get_capital(self, steam64id):
        inventory = self.client.get_partner_inventory(steam64id, self.game)
        capital = pure_assets
        tag = 'classid'
        for item in inventory.keys():
            if int(inventory[item][tag]) == item_class_ids['ref']:
                capital['metals']['ref'].append(Asset(item, self.game))
            if int(inventory[item][tag]) == item_class_ids['rec']:
                capital['metals']['rec'].append(Asset(item, self.game))
            if int(inventory[item][tag]) == item_class_ids['scrap']:
                capital['metals']['scrap'].append(Asset(item, self.game))
            if int(inventory[item][tag]) == item_class_ids['key']:
                capital['other']['key'].append(Asset(item, self.game))
        return capital

    def find_key(self, tradeurl, quantity):
        steam64id = partner_to_64id(tradeurl)
        inventory = self.client.get_partner_inventory(steam64id, self.game)
        capital, count = [], 0
        tag = 'classid'
        for item in inventory.keys():
            if count < quantity:
                if int(inventory[item][tag]) == item_class_ids['key']:
                    capital.append(Asset(item, self.game))
                    count += 1
        return capital

    def trade_for(self, price, item, partner_url):
        partner = None
        if item == 'key':
            partner = self.find_key(partner_url, 1)
            own = resize_offer(self.capital, price)
            try:
                offer = self.client.make_offer_with_url(items_from_me=own, items_from_them=partner, trade_offer_url=partner_url, 
                                                        case_sensitive=False, message='Test sending trade offers')
            except Exception as e:
                print(f'Could not send offer. \n Error message: {e}')


    def arbitrage(self, asset):
        return None
       




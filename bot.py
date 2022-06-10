from steampy.client import SteamClient, Asset
from utils import Option, item_class_ids,pure_assets, resize_offer, pure_balance
import math

class Bot:
    def __init__(self, username, password, api_key, steamguard, game):
        self.client = SteamClient(api_key)
        try:
            self.client.login(username, password, steamguard)
            print('Success')
        except:
            print('Unsuccesful')
            raise SystemError

        self.game = game
        self.capital = self.get_capital(self.client.steam_guard['steamid'])
        self.balance = pure_balance(len(self.capital['metals']['ref']), len(self.capital['metals']['rec']), len(self.capital['metals']['scrap']))

    def get_pure(self):
        return self.pure

    def get_capital(self):
        return self.capital

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

    def arbitrage(self, asset):
        # asset_class = asset.opportunity()
        # if asset_class[0]:
        #     if self.balance > asset_class[2]:
        #         print(resize_offer(self.capital, self.balance))
        #     print('Arbitrage possible, but not enough balance to transact')
        ret = resize_offer(self.capital, self.balance)
        print(ret)
        return False



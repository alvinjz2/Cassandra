from steampy.client import SteamClient
from utils import Option, item_class_ids

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
        self.capital, self.collateral = {'ref': 0, 'rec': 0, 'scrap': 0, 'key' : 0}, {}
        inventory = self.get_items()
        tag = 'classid'
        for item in inventory.keys():
            if inventory[item][tag] == '2674':
                self.capital['ref'] += 1
            if inventory[item][tag] == '5564':
                self.capital['rec'] += 1
            if inventory[item][tag] == '2675':
                self.capital['scrap'] += 1
            if inventory[item][tag] == '101785959':
                self.capital['key'] += 1
        
    def get_capital(self):
        return self.capital

    def get_items(self):
        return self.client.get_my_inventory(self.game)

    def get_partner_items(self, partner_id):
        return self.client.get_partner_inventory(partner_id, self.game)

    def arbitrage(self, asset):
        if asset[Option.opportunity]:
            return True
        return False



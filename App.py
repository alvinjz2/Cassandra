from AssetClass import AssetClass
from bot import Bot
from steampy.utils import GameOptions
import os
from dotenv import load_dotenv
from utils import request_helper, find_tf2item, partner_to_64id

load_dotenv()
username, password, api_key, path = os.environ.get('id'), os.environ.get('password'), os.environ.get('steam_api_key'), os.environ.get('guard_txt')
steven = 'https://steamcommunity.com/tradeoffer/new/?partner=164820724&token=agoMNKiO'
key = 'https://next.backpack.tf/stats?item=Mann%20Co.%20Supply%20Crate%20Key&quality=Unique'
tod = 'https://next.backpack.tf/stats?item=Tour%20of%20Duty%20Ticket&quality=Unique'
key2 = 'https://next.backpack.tf/classifieds?itemName=Mann%20Co.%20Supply%20Crate%20Key&quality=6'

a = AssetClass(key)
# b = Bot(username, password, api_key, path, GameOptions.TF2)
# # b.print()
# b.arbitrage(a)
#b.message_offer(steven, 'Buy', '1', 'Mann Co. Supply Crate Key')
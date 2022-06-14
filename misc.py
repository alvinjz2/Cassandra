from enum import Enum
class Option(Enum):
    opportunity = 0
    bid = 1
    ask = 2
    bid_currency = 3
    ask_currency = 4
    bid_url = 5
    ask_url = 6
    bid_64id = 7
    ask64_id = 8
   
# Look to implement database catalog with name/ids in the future
item_class_ids = {'scrap': 2675, 'key': 101785959, 'ref': 2674, 'rec': 5564, '2675': 'scrap', '101785959' : 'key', '2674' : 'ref', '5564' : 'rec'}
currency = ['ref', 'rec', 'scrap', 'key']
pure_assets = {'metals': {'ref': [], 'rec': [], 'scrap': []}, 'other': {'key' : []}}
REC_VALUE = 0.33
SCRAP_VALUE = 0.11
from enum import Enum

def partner_to_64id(trade_url):
    x = trade_url.split('?')[1].split('&')[0].split('=')[1]
    return (1 << 56) | (1 << 52) | (1 << 32) | int(x)
    
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
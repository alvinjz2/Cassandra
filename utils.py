from enum import Enum
import math
def partner_to_64id(trade_url):
    x = trade_url.split('?')[1].split('&')[0].split('=')[1]
    return str((1 << 56) | (1 << 52) | (1 << 32) | int(x))

def pure_balance(ref, rec, scrap):
    rem_scrap = scrap % 3
    t_rec = rec + scrap // 3
    rem_rec = t_rec % 3
    t_ref = ref + t_rec // 3
    return t_ref + REC_VALUE * rem_rec + SCRAP_VALUE * rem_scrap

def resize_offer(capital, val):
    frac, whole = math.modf(val)
    frac = round(frac, 2)
    ref, rec, scrap = [], [], []
    for rec_asset in capital['metals']['rec']:
        if frac - REC_VALUE > 0:
            frac -= REC_VALUE
            frac = round(frac, 2)
            rec.append(rec_asset)
            capital['metals']['rec'].pop(0)
    for scrap_asset in capital['metals']['scrap']:
        if frac - SCRAP_VALUE >= 0:
            frac -= SCRAP_VALUE
            frac = round(frac, 2)
            scrap.append(scrap_asset)
            capital['metals']['scrap'].pop(0)
    ref = capital['metals']['ref'][0 : int(whole)]
    capital['metals']['ref'] = capital['metals']['ref'][int(whole) :]
    return ref + rec + scrap

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
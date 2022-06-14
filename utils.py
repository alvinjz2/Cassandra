import math
import requests
from misc import REC_VALUE, SCRAP_VALUE, pure_assets, item_class_ids
from steampy.utils import GameOptions
from steampy.client import Asset

def partner_to_64id(trade_url):
    x = trade_url.split('?')[1].split('&')[0].split('=')[1]
    return str((1 << 56) | (1 << 52) | (1 << 32) | int(x))


def pure_balance(steam64id):
    capital = get_tf2capital(steam64id)
    ref, rec, scrap = len(capital['metals']['ref']), len(capital['metals']['rec']), len(capital['metals']['scrap'])
    rem_scrap = scrap % 3
    t_rec = rec + scrap // 3
    rem_rec = t_rec % 3
    t_ref = ref + t_rec // 3
    return t_ref + REC_VALUE * rem_rec + SCRAP_VALUE * rem_scrap


def find_tf2item(steam64id, quantity, id):
    inventory = requests.get(f'https://steamcommunity.com/inventory/{steam64id}/440/2?l=english&count=5000').json()
    items, count = [], 0
    for item in inventory['assets']:
        if count >= quantity:
            break
        if int(item['classid']) == item_class_ids[id]:
            items.append(Asset(item['assetid'], GameOptions.TF2))
            count += 1
    return items


def get_tf2capital(steam64id):
    inventory = requests.get(f'https://steamcommunity.com/inventory/{steam64id}/440/2?l=english&count=5000').json()
    inv, game = pure_assets, GameOptions.TF2
    for item in inventory['assets']:
        if int(item['classid']) == item_class_ids['ref']:
            inv['metals']['ref'].append(Asset(item['assetid'], game))
        if int(item['classid']) == item_class_ids['rec']:
            inv['metals']['rec'].append(Asset(item['assetid'], game))
        if int(item['classid']) == item_class_ids['scrap']:
            inv['metals']['scrap'].append(Asset(item['assetid'], game))
        if int(item['classid']) == item_class_ids['key']:
            inv['other']['key'].append(Asset(item['assetid'], game))
    return inv


def resize_offer(capital, val):
    frac, whole = math.modf(val)
    frac = round(frac, 2)
    ref, rec, scrap = [], [], []
    for rec_asset in capital['metals']['rec']:
        if frac - REC_VALUE > 0:
            frac -= REC_VALUE
            frac = round(frac, 2)
            rec.append(rec_asset)
        else:
            break
    for scrap_asset in capital['metals']['scrap']:
        if frac - SCRAP_VALUE > 0:
            frac -= SCRAP_VALUE
            frac = round(frac, 2)
            scrap.append(scrap_asset)
        else:
            break
    ref = capital['metals']['ref'][0 : int(whole)]
    return ref + rec + scrap

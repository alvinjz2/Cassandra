def partner_to_64id(trade_url):
    x = trade_url.split('?')[1].split('&')[0].split('=')[1]
    return (1 << 56) | (1 << 52) | (1 << 32) | int(x)
    

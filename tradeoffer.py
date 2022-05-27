import os
import json
from dotenv import load_dotenv
load_dotenv()

import steam
import steam.webauth as wa
from steam.client import SteamClient
from steam.guard import SteamAuthenticator
username, password = os.environ.get('username'), os.environ.get('password')

secret = json.load(open(os.environ.get('location')))
sa = SteamAuthenticator(secret)
tfa = sa.get_code()

user = wa.WebAuth(username)
try:
    user.login(password)
except (wa.CaptchaRequired, wa.LoginIncorrect) as exp:
    if isinstance(exp, wa.LoginIncorrect):
        print('Wrong password.')
    else:
        password = password

    if isinstance(exp, wa.CaptchaRequired):
        print('Solve captcha.')
        # ask a human to solve captcha
    else:
        captcha = None

    user.login(password=password, captcha=captcha)
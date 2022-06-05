import os
import json
from steam.guard import SteamAuthenticator
from steam.client import SteamClient
from dotenv import load_dotenv

load_dotenv()
username, password = os.environ.get('id'), os.environ.get('password')
secrets = json.load(open('steamguard.json'))
sa = SteamAuthenticator(secrets)
tfa = sa.get_code()

client = SteamClient()

try:
    client.login(username=username, password=password, two_factor_code=tfa)
    print('Success')
except:
    print('Could not login')


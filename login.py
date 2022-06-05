import os
from dotenv import load_dotenv
load_dotenv()
username, password, api_key = os.environ.get('id'), os.environ.get('password'), os.environ.get('steam_api_key')

from steampy.client import SteamClient
client = SteamClient(api_key)
try:
    client.login(username, password, os.environ.get('guard_txt'))
    print('Success')
except:
    print('Could not login')
    raise SystemError


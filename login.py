import os
import json
from dotenv import load_dotenv
load_dotenv()

from steam.client import SteamClient
from steam import guard

username, password = os.environ.get('username'), os.environ.get('password')
client = SteamClient()
secret = json.load(open(os.environ.get('secrets')))
SA = guard.SteamAuthenticator(secret)
result = client.login(username=username, password=password, two_factor_code=SA.get_code())
print(result)

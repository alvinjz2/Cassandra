import os
import steam.webauth as wa
from dotenv import load_dotenv

load_dotenv()
user = wa.WebAuth(os.environ.get("id"))

try:
    session = user.cli_login(os.environ.get("password"))
    session.get('https://store.steampowered.com/account/history')
    print('Success')
except:
    print('Unable to get session')
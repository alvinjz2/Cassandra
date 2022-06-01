import os
import json
from dotenv import load_dotenv
load_dotenv()

import steam
import steam.webauth as wa
from steam.client import SteamClient
from steam.guard import SteamAuthenticator
from steam.enums import EResult
from steam import guard
username, password = os.environ.get('username'), os.environ.get('password')

client = SteamClient()

secret = json.load(open(os.environ.get('location')))
SA = guard.SteamAuthenticator(secret)
tfa = SA.get_code()


client = SteamClient()

@client.on("error")
def handle_error(result):
    print("\nError", result)

@client.on("connected")
def handle_connected():
    print("\nConnected to", client.current_server_addr, "\n")

@client.on("reconnect")
def handle_reconnect(delay):
    print("\nReconnect in", delay, "seconds...")

@client.on("disconnected")
def handle_disconnect():
    print("\nDisconnected.")

    if client.relogin_available:
        print("\nReconnecting...")
        client.reconnect(maxdelay=30)

@client.on("logged_on")
def handle_after_logon():
    print("Logged on as:", client.user.name)
    print("\nAuto accept friend requests is enabled.")
    print("Auto message is enabled.")
    print("-"*20)
    print("Press ^C to exit")

try:
    result = client.login(username=username, password=password, two_factor_code=SA.get_code())

    if result != EResult.OK:
        print("Failed to login:", repr(result))
        raise SystemExit
    
    client.run_forever()

except KeyboardInterrupt:
    if client.connected:
        print("Logout")
        client.logout()
    raise SystemExit
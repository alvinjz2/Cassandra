import os
import asyncio
from dotenv import load_dotenv

load_dotenv()
steamguard = {
    "steamid": "wxlydf",
    "shared_secret": "UmHpWrsHMOUgWfjncJBobD8iqds=",
    "identity_secret": "i48bNdh8nEI8J2j99SzQBBSsAo4=",
}
from asyncsteampy.client import SteamClient as AsyncSteamClient
username, password, api_key = os.environ.get('username'), os.environ.get('password'), os.environ.get('steam_api_key')


async def signin(username, password, steamguard, api_key):
    async_steam_client = AsyncSteamClient(username, password, steamguard, api_key=api_key)
    try:
        await async_steam_client.login()
        print('Success')
        await async_steam_client.close()
    except:
        print('Unsuccessful')
        await async_steam_client.close()


asyncio.run(signin(username, password, steamguard, api_key))
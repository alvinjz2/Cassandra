from steampy.client import SteamClient

class Bot:
    def __init__(self, username, password, api_key, steamguard):
        self.client = SteamClient(api_key)
        try:
            self.client.login(username, password, steamguard)
            print('Success')
        except:
            print('Unsuccesful')
            raise SystemError
            
    def __del__(self):
        self.client.logout()

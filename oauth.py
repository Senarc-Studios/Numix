import requests

class Oauth:
    client_id = "744865990810271785" # Your Client ID here
    client_secret = "imKDsftXGNQ9WkGgbQ5U6i2XOFOzbg_B" # Your Client Secret here
    redirect_uri = "https://dash.numix.xyz/login"
    scope = "identify%20email%20guilds"
    discord_login_url = "https://discord.com/api/oauth2/authorize?client_id=744865990810271785&redirect_uri=https%3A%2F%2Fdash.numix.xyz%2Flogin&response_type=code&scope=identify%20email%20guilds" # Paste the generated Oauth2 link here
    discord_token_url = "https://discord.com/api/oauth2/token"
    discord_api_url = "https://discord.com/api"
 
    @staticmethod
    def get_access_token(code):
        payload = {
            "client_id": Oauth.client_id,
            "client_secret": Oauth.client_secret,
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": Oauth.redirect_uri,
            "scope": Oauth.scope
        }
 
        access_token = requests.post(url = Oauth.discord_token_url, data = payload).json()
        return access_token.get("access_token")

    @staticmethod
    def get_user_json(access_token):
        url = f"{Oauth.discord_api_url}/users/@me"
        headers = {"Authorization": f"Bearer {access_token}"}
 
        user_object = requests.get(url = url, headers = headers).json()
        return user_object






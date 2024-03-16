import aiohttp
from utils.api_variables import url_auth, url_logout
import time
import json

def login_and_extract_token(username, password):
    """Login to the website and extract JWT token."""
    async with aiohttp.ClientSession() as session:
        async with session.post(
            "https://api-edu.skysmart.ru/api/v1/user/registration/teacher", 
            data=json.dumps({
                "userAgent":{
                    "ua":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
                    "browser":{"name":"Chrome","version":"122.0.0.0","major":"122"},
                    "engine":{"name":"Blink","version":"122.0.0.0"},
                    "os":{"name":"Windows","version":"10"},
                    "device":{},"cpu":{"architecture":"amd64"}
                }
            })
        ) as resp:
            json_resp = await resp.json()
            token = json_resp["jwtToken"]
            save_token_to_json(token)
            return token
    
def save_token_to_json(token, filename="token.json"):
    """Save the token to a JSON file."""
    try:
        with open(filename, "w") as file:
            json.dump({"token": token}, file, indent=4)
        return True
    except Exception as e:
        return False

def get_token():
    token = login_and_extract_token(auth_creds['username'], auth_creds['password'])
    if token:
        success = save_token_to_json(token)   
        return success
    return False

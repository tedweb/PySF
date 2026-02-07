import os
import requests
import constants

cli_params = [
    {
        "name": "Login URL",
        "field": "login_url",
        "default": "https://login.salesforce.com/services/oauth2/token"
    }, {
        "name": "User Name",
        "field": "username",
        "default": ""
    }, {
        "name": "User Password",
        "field": "password",
        "default": ""
    }, {
        "name": "Consumer Key",
        "field": "client_id",
        "default": ""
    }, {
        "name": "Consumer Secret",
        "field": "client_secret",
        "default": ""
    }, {
        "name": "Security Token",
        "field": "security_token",
        "default": ""
    }
]

def get_params_from_env_vars(org):
    login_url = f"{constants.DEFAULT_PROTOCOL}{constants.DEFAULT_URL}"
    auth_path = constants.DEFAULT_AUTH_PATH
    consumer_key = ''
    consumer_secret = ''

    if 'params' in org:
        if 'login_url' in org['params']:
            login_url = os.getenv(org["params"]["login_url"])
            if login_url.find('://') < 0:
                login_url = f"{constants.DEFAULT_PROTOCOL}{login_url}"
        if 'auth_path' in org['params']:
            auth_path = os.getenv(org['params']['auth_path'])
        if 'consumer_key' in org['params']:
            consumer_key = os.getenv(org['params']['consumer_key'])
        if 'consumer_secret' in org['params']:
            consumer_secret = os.getenv(org['params']['consumer_secret'])

    return {
        "grant_type": "client_credentials", # Grant Type
        "login_url": login_url,
        "auth_path": auth_path,
        "client_id": consumer_key, # Consumer Key
        "client_secret": consumer_secret # Consumer Secret
    }

def get_authentication(org):
    request_params = {
        'grant_type': org['params']['grant_type'],
        'client_id': org['params']['client_id'],
        'client_secret': org['params']['client_secret']
    }
    response = requests.post(f"{org['params']['login_url']}{org['params']['auth_path']}", params=request_params).json()

    message = ''
    if response.get("access_token"):
        message = f"Successfully connected to '{org['name']}"
    else:
        message = f"Error connecting to '{org['name']}':\n  Message: '{response.get('error_description')}'"

    return {
        "connection_name": org['name'],
        "access_token": response.get("access_token"),
        "instance_url": response.get("instance_url"),
        "id": response.get("id"),
        "token_type": response.get("token_type"),
        "issued_at": response.get("issued_at"),
        "signature": response.get("signature"),
        "message": message
    }
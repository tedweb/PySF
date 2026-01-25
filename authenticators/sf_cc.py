import os
import requests

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
    login_url_key = org["params"]["login_url"]
    auth_path_key = org["params"]["auth_path"]
    consumer_key = org["params"]["consumer_key"]
    consumer_secret_key = org["params"]["consumer_secret"]
    return {
        "grant_type": "client_credentials", # Grant Type
        "login_url": os.getenv(login_url_key),
        "auth_path": os.getenv(auth_path_key),
        "client_id": os.getenv(consumer_key), # Consumer Key
        "client_secret": os.getenv(consumer_secret_key) # Consumer Secret
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
        message = f"Error connecting to '{org['name']}'. Message: '{response.get('error_description')}'"

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
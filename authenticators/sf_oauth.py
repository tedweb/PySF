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
    user_name_key = org["params"]["username"]
    user_password_key = org["params"]["password"]
    security_token_key = org["params"]["security_token"]
    consumer_key = org["params"]["consumer_key"]
    consumer_secret_key = org["params"]["consumer_secret"]
    return {
        "grant_type": "password", # Grant Type
        "client_id": os.getenv(consumer_key), # Consumer Key
        "client_secret": os.getenv(consumer_secret_key), # Consumer Secret
        "username": os.getenv(user_name_key), # Dedicated integration user username
        "password": os.getenv(user_password_key), # Dedicated integration user password
        "security_token": os.getenv(security_token_key) # Dedicated integration user security token
    }

def get_authentication(org):
    request_params = {
        'username': org['params']['username'],
        'client_id': org['params']['client_id'],
        'client_secret': org['params']['client_secret'],
        'password': f"{org['params']['password']}{org['params']['security_token']}",
        'grant_type': org['params']['grant_type']
    }
    response = requests.post(f"{org['login_url']}{org['authentication']['path']}", params=request_params).json()

    message = ''
    if response.get("access_token"):
        message = f"Successfully connected to '{org['name']}' as user {org['params']['username']}"
    else:
        message = f"Error connecting to '{org['name']}'. Message: '{response.get('error_description')}'"

    return {
        "connection_name": org['name'],
        "user_name": org['params']['username'],
        "access_token": response.get("access_token"),
        "instance_url": response.get("instance_url"),
        "path": org['authentication']['path'],
        "id": response.get("id"),
        "token_type": response.get("token_type"),
        "issued_at": response.get("issued_at"),
        "signature": response.get("signature"),
        "message": message
    }
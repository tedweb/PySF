import jwt
import time
import requests
import os

cli_params = [
    {
        "name": "Login URL",
        "field": "login_url",
        "default": "https://login.salesforce.com"
    }, {
        "name": "Grant Type",
        "field": "grant_type",
        "default": "jwt"
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
    key_file_key = org["params"]["key_file"]
    user_name_key = org["params"]["username"]
    issuer_key = org["params"]["issuer"]
    return {
        "login_url": os.getenv(login_url_key),
        "auth_path": os.getenv(auth_path_key),
        "key_file": os.getenv(key_file_key),
        "username": os.getenv(user_name_key), # Dedicated integration user username
        "issuer": os.getenv(issuer_key)
    }

def get_authentication(org):
    request_params = {
        'aud': org['params']['login_url'],
        'iss': org['params']['issuer'],
        'exp': int(time.time()) + 300,
        'sub': org['params']['username']
    }

    with open(org['params']['key_file']) as fd:
        private_key = fd.read()

    encoded = jwt.encode(request_params, private_key, algorithm='RS256')

    response = requests.post(
        url = f"{org['params']['login_url']}{org['params']['auth_path']}",
        data = {
            'grant_type': 'urn:ietf:params:oauth:grant-type:jwt-bearer',
            'assertion': encoded
        }
    ).json()

    message = ''
    if response.get("access_token"):
        message = f"Successfully connected to '{org['name']}' as user {org['params']['username']}"
    else:
        message= f"Error connecting to '{org['name']}'. Message: '{response['error_description']}'"

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
import jwt
import time
import requests
import os
import constants

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
    login_url = f"{constants.DEFAULT_PROTOCOL}{constants.DEFAULT_URL}"
    auth_path = constants.DEFAULT_AUTH_PATH
    consumer_key = ''
    key_file = ''
    user_name = ''

    if 'params' in org:
        if 'login_url' in org['params']:
            login_url = os.getenv(org["params"]["login_url"])
            if login_url.find('://') < 0:
                login_url = f"{constants.DEFAULT_PROTOCOL}{login_url}"
        if 'auth_path' in org['params']:
            auth_path = os.getenv(org['params']['auth_path'])
        if 'consumer_key' in org['params']:
            consumer_key = os.getenv(org['params']['consumer_key'])
        if 'key_file' in org['params']:
            key_file = os.getenv(org['params']['key_file'])
        if 'user_name' in org['params']:
            user_name = os.getenv(org['params']['user_name'])
        if 'username' in org['params']:
            user_name = os.getenv(org['params']['username'])

    return {
        "login_url": login_url,
        "auth_path": auth_path,
        "key_file": key_file,
        "username": user_name, # Dedicated integration user username
        "issuer": consumer_key
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
        message= f"Error connecting to '{org['name']}':\n  Message: '{response['error_description']}'"

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
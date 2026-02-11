import jwt
import time
import requests
import constants

cli_params = [
    {
        "name": "Login URL",
        "field": "login_url",
        "default": constants.DEFAULT_URL
    },{
        "name": "User Name",
        "field": "user_name",
        "default": ""
    },{
        "name": "Consumer Key",
        "field": "consumer_key",
        "default": ""
    },{
        "name": "Path to *.crt file",
        "field": "key_file",
        "default": ""
    }
]

def get_authentication(org):
    request_params = {
        'aud': org['params']['login_url']['value'],
        'iss': org['params']['consumer_key']['value'],
        'exp': int(time.time()) + 300,
        'sub': org['params']['user_name']['value']
    }

    with open(org['params']['key_file']['value']) as fd:
        private_key = fd.read()
    encoded = jwt.encode(request_params, private_key, algorithm='RS256')

    response = requests.post(
        url = f"{org['params']['login_url']['value']}{constants.DEFAULT_AUTH_PATH}",
        data = {
            'grant_type': constants.GRANT_TYPE_JWT,
            'assertion': encoded
        }
    ).json()

    message = ''
    if response.get("access_token"):
        message = f"successfully connected to {org['params']['login_url']['value']} as user {org['params']['user_name']['value']}"
    else:
        message = f"error connecting to {org['params']['login_url']['value']}:\n  Message: '{response['error_description']}'"

    return {
        "connection_name": '' if 'name' not in org else org['name'],
        "access_token": response.get("access_token"),
        "instance_url": response.get("instance_url"),
        "id": response.get("id"),
        "token_type": response.get("token_type"),
        "issued_at": response.get("issued_at"),
        "signature": response.get("signature"),
        "message": message
    }
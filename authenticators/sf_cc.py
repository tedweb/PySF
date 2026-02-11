import requests
import constants

cli_params = [
    {
        "name": "Login URL",
        "field": "login_url",
        "default": constants.DEFAULT_URL
    }, {
        "name": "Consumer Key",
        "field": "consumer_key",
        "default": ""
    }, {
        "name": "Consumer Secret",
        "field": "consumer_secret",
        "default": ""
    }
]

def get_authentication(org):
    request_params = {
        'grant_type': constants.GRANT_TYPE_CC,
        'client_id': org['params']['consumer_key']['value'],
        'client_secret': org['params']['consumer_secret']['value']
    }
    auth_path = f"{org['params']['login_url']['value']}{constants.DEFAULT_AUTH_PATH}"
    response = requests.post(auth_path, params=request_params).json()

    message = ''
    if response.get("access_token"):
        message = f"successfully connected to {org['params']['login_url']['value']}"
    else:
        message = f"error connecting to {org['params']['login_url']['value']}:\n  Message: '{response.get('error_description')}'"

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
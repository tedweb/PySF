import sf_cc
import sf_jwt
import constants, util

auth_methods = {
    'cc': sf_cc,
    'jwt': sf_jwt
}
org_list = None
auth_method = None

def get_org_listing(config):
    global org_list
    org_list = config['orgs']

    if org_list is not None:
        org_names = []
        for index in range(len(org_list)):
            org_names.append(f"{org_list[index]['name']}")
        return org_names
    return []

def authenticate(org):
    global auth_method
    util.animate_msg('Authenticating')
    if 'grant_type' in org and org['grant_type'] in auth_methods:
        if org['params']['login_url']['value'].find('://') < 0:
            org['params']['login_url']['value'] = f"{constants.DEFAULT_PROTOCOL}{org['params']['login_url']['value']}"
        auth_method = auth_methods[org['grant_type'].lower()] # This is either sf_cc.py or sf_jwt.py
        org['authentication'] = auth_method.get_authentication(org)
    return org

def get_auth_method_params(method):
    auth_method = auth_methods[method]
    return auth_method.cli_params

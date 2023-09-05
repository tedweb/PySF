import sf_oauth
import sf_jwt
import sys, time

auth_methods = {
    'oauth': sf_oauth,
    'jwt': sf_jwt
}
org_list = None
auth_method = None
default_grant_type = 'oauth'

def get_org_listing(config):
    global org_list
    org_list = config['orgs']
    org_names = []
    for index in range(len(org_list)):
        org_names.append(org_list[index]['name'])
    return org_names

def authenticate_org(org_index):
    global auth_method
    org = {}
    iterations = 3

    for i in range(iterations+1):
        sys.stdout.write(f"\rAuthenticating{'.' * i}")
        time.sleep(0.35)
        sys.stdout.flush()
    sys.stdout.write(f"\rAuthenticating{'.' * i} ")

    if org_index < len(org_list):
        org = org_list[org_index].copy()
        grant_type = org['grant_type']
        auth_method = auth_methods[grant_type]
        org['params'] = auth_method.get_params_from_env_vars(org)
    else:
        grant_type = input (f"  Grant Type [{default_grant_type}]: ")
        org['grant_type'] = grant_type if grant_type != '' else default_grant_type
        auth_method = auth_methods[org['grant_type']]
        return load_params_from_user(org)

    org['authentication'] = auth_method.get_authentication(org)
    return org

def load_params_from_user(org):
    org['params'] = {}

    for param_index in range(len(auth_method.cli_params)):
        param = auth_method.cli_params[param_index]
        default = f" [{param['default']}]" if param['default'] != '' else ''
        entry = input (f"  {param['name']}{default}: ")
        entry = entry if entry != '' else param['default']
        if param_index < 1:
            org[param['field']] = entry
        else:
            org['params'][param['field']] = entry
    return org

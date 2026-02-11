import apis.rest as api
from authenticators import sf_auth
import util, constants
import importlib, sys, time, copy, os

splash_screen = '''
                  %@@@@&@@&@@@&*    .#&@&&&&(
               #@@%           .&@@@@&,      *&@@#
              @@/                               @@@@@@@@@@@&%
             &@                                             /&@&.
            *@&                                                %@&
             @@      @@,@@@            .@@@@@   @@@@@@@          &@.
            %@@&     @@   @@ /@&   @@  @@       @@               ,@&
          &@&        @@ @@(   #@/ @@    ,@@@@   @@@@@@,           @@
         @@%         @@        &@@@         @@  @@               #@&
         @&          @@         @@.    ,@@@@.   @@              (@&
         @@                   @@@                             *@@%
         ,@@                                              .&@@@,
           &@@(                                   %@@&@@&&#.
              %&@@@@@@%                #&&/..,(&@@&
                     &@&              @@& ,/(/.
                       #@@&#.    .%&@@#
                           ,#@&&&#,

                      Python Interface for Salesforce
                              ©2023 Ted Godwin
'''
org = None
config = None
command_listing = [
    'REST: Query an object',
    'SOAP: Query an object',
    'GraphQL: Query an object',
    'BULK: Insert records',
    'Listen for events via Pub/Sub API',
    'Kick off a Flow'
]
operation_listing = [
    'Search for records',
    'Create new record',
    'Update a record',
    'Delete a record'
]

def do_continue(arg):
    if str(arg).upper() != 'B':
        return True
    else:
        command_path.pop()
        command_path[len(command_path)-1]()

def display_splash():
    global command_path
    global config
    command_path = []
    print(f"{splash_screen}")
    util.load_env_vars()
    command_path.append(display_connection_options)
    config = util.load_config()
    if config is None:
        config = {}
    if 'orgs' not in config:
        config['orgs'] = []

def display_connection_options():
    org_listing = sf_auth.get_org_listing(config)
    if len(org_listing) > 0:
        print("\nAvailable Salesforce connections:")
    else:
        print("\nNo Salesforce connections available:")
    selection = util.get_selection(org_listing, f"(Q)uit, (C)reate, (E)dit, (D)elete or select a connection 1-{len(org_listing)}: ", 1, ['c', 'e', 'd'])

    if type(selection) is int:
        load_saved_org_by_name(org_listing[selection])

    if type(selection) is str:
        selection = selection.lower()
        if selection == 'c':
            load_new_org_from_cli()
        elif selection == 'e':
            print(constants.UNDER_CONSTRUCTION)
        elif selection == 'd':
            print(constants.UNDER_CONSTRUCTION)

def load_new_org_from_cli():
    global org
    org = {}
    org['params'] = {}
    print("\nAvailable authentication methods:")
    selection = util.get_selection(constants.AUTH_TYPES, None, 1)
    if selection.lower() != 'b':
        org['grant_type'] = 'jwt' if selection != 0 else constants.DEFAULT_GRANT_TYPE
        auth_params = sf_auth.get_auth_method_params(org['grant_type'])

        print("\nRequired org credentials:")
        for param_index in range(len(auth_params)):
            param = auth_params[param_index]
            message = f" {param['name']} [{param['default']}]: " if param['default'] != '' else f" {param['name']}: "
            value = input(message)
            value = value if value != '' else param['default']
            if do_continue(value):
                org['params'][param['field']] = {
                    'key': util.get_uuid(),
                    'value': value
                }
        authenticate()

def load_saved_org_by_name(name):
    global org
    org_list = config['orgs']
    orgs = [item for item in org_list if item['name'] == name]
    org = orgs[0] if len(orgs) > 0 else None
    if org is not None:
        auth_params = sf_auth.get_auth_method_params(org['grant_type'])
        for param_index in range(len(auth_params)):
            param = auth_params[param_index]
            field_name = param['field']
            key_value = org['params'][field_name]
            if type(org['params'][field_name]) is str:
                org['params'][field_name] = {
                    'key': key_value,
                    'value': os.getenv(key_value)
                }
    authenticate()

def authenticate():
    global org
    org = sf_auth.authenticate(org)
    print(f"{org['authentication']['message']}")
    login_success = org['authentication']['access_token'] is not None
    login_saved = 'name' in org and org['name'] != ''
    if login_success:
        util.save_access_token(org, config) # under construction
    if login_success and login_saved: 
        command_path.append(load_command)
    elif login_success and not login_saved: 
        prompt_to_save_org()

def prompt_to_save_org():
    print("\nSave org?")
    caption = '  Save this org for future use? (Y)es or (N)o: '
    do_proceed = input(caption)
    while do_proceed.upper() not in ['Y', 'N']:
        util.reset_entry(caption)
        do_proceed = input(caption)

    if do_proceed.upper() == 'Y':
        caption = '  Name of connection: '
        org_name = input(caption)
        while org_name.strip() == '':
            util.reset_entry(caption)
            org_name = input(caption)
        org['name'] = org_name

        new_org = copy.deepcopy(org)
        new_org.pop('authentication')
        for param in new_org['params'].keys():
            new_org['params'][param] = new_org['params'][param]['key']
        if config['orgs'] is None:
            config['orgs'] = []
        config['orgs'].append(new_org)
        util.save_config(config)
        util.save_env(org)

        iterations = 3
        for i in range(iterations+1):
            sys.stdout.write(f"\rSaving{'.' * i}")
            time.sleep(0.35)
            sys.stdout.flush()
        sys.stdout.write(f"\rSaving{'.' * i} done!\n")
    command_path.append(load_command)

def load_command():
    global command_index
    print(f"\nCommands:")
    selection = util.get_selection(command_listing, None, 1)
    if do_continue(selection):
        print(f"Selected Command: '{command_listing[selection]}'\r\n")
        command_path.append(load_entity)

def load_entity():
    global entity
    print("Salesforce Entities:")
    entity_listing = api.get_entity_listing(org)
    selection = util.get_selection(entity_listing, None, 4)
    if do_continue(selection):
        entity_name = entity_listing[selection]
        entity = importlib.import_module(f'entities.{entity_name.lower()}')
        print(f"Selected Entity: '{entity_name}'\r\n")
        command_path.append(load_operation)

def load_operation():
    print("Command Operations:")
    selection = util.get_selection(operation_listing, None, 0)
    if do_continue(selection):
        operation_name = operation_listing[selection].lower()
        if "search" in operation_name:
            command_path.append(search_records)
        elif "create" in operation_name:
            command_path.append(create_record)
        elif "update" in operation_name:
            command_path.append(update_record)
        elif "delete" in operation_name:
            command_path.append(delete_record)
        print(f"Selected Operation: '{operation_name.capitalize()}'\r\n")

def create_record():
    print(f"Create New {entity.name} Record")
    payload = util.get_payload(entity.target_fields)
    result = api.post(org, entity.name, payload)
    if len(result['items']) > 0:
        print(f"New {entity.name} record created with an id of {result['items'][0]['id']}")
    elif result['message'] != '':
        print(result['message'])
    command_path.pop()
    input("Press 'Enter' to continue:")
    print("\r\n")

def search_records():
    print(f"Search for Existing {entity.name} Record")
    entry = input("Search Criteria: ").upper()
    result = api.get(org, entity.name, fields=entity.target_fields, search_criteria=entry)
    if len(result['items']) > 0:
        print(util.format_get(result['items'], entity.target_fields))
    elif result['message'] != '':
        print(result['message'])
    else:
        print("No matching records discovered.")
    command_path.pop()
    input("Press 'Enter' to continue:")
    print("\r\n")

def update_record():
    print(f"Update Existing {entity.name} Record")
    target_id = util.get_payload(['Id'], existing_record = {})['Id']
    target_record = api.get(org, entity.name, id=target_id)
    if (len(target_record['items']) > 0):
        print("\r\nPressing 'Enter' accepts existing values...")
        payload = util.get_payload(entity.target_fields, existing_record = target_record['items'][0])
        if payload is not None:
            result = api.patch(org, entity.name, target_id, payload)
            if len(result['items']) > 0:
                print(f"{entity.name} record successfully updated!")
            else:
                print(result['message'])
        else:
            print('Update cancelled.')
    else:
        print(f"No {entity.name} record found with Id of '{target_id}'.")  
    command_path.pop()
    input("Press 'Enter' to continue:")
    print("\r\n")

def delete_record():
    print(f"Delete Existing {entity.name} Record")
    target_id = util.get_payload(['Id'], existing_record = {})['Id']
    result = api.get(org, entity.name, id=target_id)
    if len(result['items']) > 0:
        print(util.format_get(result['items'], entity.target_fields))
        caption = 'Delete? (Y)es or (N)o: '
        do_proceed = input(caption)
        while do_proceed.upper() not in ['Y', 'N']:
            util.reset_entry(caption)
            do_proceed = input(caption)
        if do_proceed.upper() == 'Y':
            result = api.delete(org, entity.name, target_id)
            print(f"Successfully deleted {entity.name} record with id of {target_id}!")
    elif result['message'] != '':
        print(result['message'])
    else:
        print("No matching records discovered.")
    command_path.pop()
    input("Press 'Enter' to continue:")
    print("\r\n")

if __name__ == "__main__":
    display_splash()
    while len(command_path) > 0:
        command_path[len(command_path)-1]()
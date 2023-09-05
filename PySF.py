import apis.rest as api
from authenticators import sf_auth
import util
import importlib

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
                             ©2023 by Ted Godwin
'''
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
    print("\r\n")
    command_path.pop()
    command_path[len(command_path)-1]()

def display_splash():
  global command_path
  global config
  command_path = []
  print(f"{splash_screen}")
  util.load_env_vars()
  command_path.append(load_connection)
  config = util.load_config()

def load_connection():
  global org
  print("Available Salesforce Connections:")
  org_listing = sf_auth.get_org_listing(config)
  selection = util.get_selection(org_listing, f"(Q)uit or select an option 1-{len(org_listing)}: ")
  org = sf_auth.authenticate_org(selection)
  print(f"{org['authentication']['message']}\r\n")
  command_path.append(load_command)

def load_command():
  global command_index
  print(f"Commands:")
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
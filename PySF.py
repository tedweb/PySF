from apis import rest
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
  entity_listing = rest.get_entity_listing(org)
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
    operation_name = operation_listing[selection]
    print(f"Selected Operation: '{operation_name}'\r\n")
    command_path.append(search_records)

def search_records():
  entry = input("Search Criteria: ").upper()
  result = rest.get(org, entity.name, entity.target_fields, entry)
  print(result)
  command_path.pop()
  input("Press 'Enter' to continue:")
  print("\r\n")

if __name__ == "__main__":
  display_splash()
  while len(command_path) > 0:
    command_path[len(command_path)-1]()
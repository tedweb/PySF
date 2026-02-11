
import os, sys, time, math, yaml, uuid
import constants
from os import path
from dotenv import load_dotenv

source_path = os.path.dirname(os.path.realpath(__file__))
resource_path = os.path.join(source_path, constants.RESOURCE_FOLDER)

def load_env_vars():
    load_dotenv(path.join(resource_path, constants.ENVIRONMENT_FILE))

def load_config():
    config_file = os.path.join(resource_path, constants.CONFIG_FILE)
    with open(config_file, "r") as yml_file:
        config = yaml.load(yml_file, Loader=yaml.FullLoader)
    return config

def get_uuid():
    return str(uuid.uuid4())

def save_config(config):
    config_file = os.path.join(resource_path, constants.CONFIG_FILE)
    with open(config_file, 'w') as file:
        yaml.dump(config, file)

def save_env(org):
    env_file = os.path.join(resource_path, constants.ENVIRONMENT_FILE)
    with open(env_file, "a") as file:
        for param in org['params'].keys():
            file.write(f"{org['params'][param]['key']} = {org['params'][param]['value']}\n")

def save_access_token(org, config):
    # print(constants.UNDER_CONSTRUCTION)
    x = 1

def get_selection(listings, caption=None, max_cols=5, alt_listings=None):
    min_count = 5
    list = []
    if len(listings) <= min_count:
        index = 1
        for listing in listings:
            list.append(f"  {index}) {listing}")
            index = index + 1
    else:
        row_count = math.ceil(len(listings) / max_cols)
        list = [""] * row_count
        size = os.get_terminal_size()
        col_width = math.floor(size.columns/max_cols)
        list_queue = listings.copy()
        listing_index = 0
        while len(list_queue) > 0:
            for row_index in range(row_count):
                if len(list_queue) > 0:
                    listing_index = listing_index + 1
                    listing_index_width = 5
                    listing = f"{listing_index}) ".rjust(listing_index_width)
                    listing = f"{listing}{list_queue.pop(0)}"
                    if len(listing) >= col_width:
                        listing = f"{listing[0:col_width-listing_index_width]}..."
                    listing = listing.ljust(col_width)
                    list[row_index] = f"{list[row_index]}{listing}"

    for index in range(len(list)):
        print(list[index])

    if not caption:
        caption = f"(B)ack, (Q)uit or select an option 1-{len(listings)}: "

    if alt_listings:
        for index in range(len(alt_listings)):
            alt_listings[index] = alt_listings[index].upper()
        
    result = None
    while result is None:
        entry = input(caption).upper()
        if entry.isnumeric() and int(entry)<=len(listings):
            result = int(entry)-1
        elif entry == 'B':
            result = entry
        elif entry == 'Q':
            shutdown(0)
        elif entry in alt_listings:
            result = entry
        else:
            reset_entry(caption)
    return result

def get_payload(fields=[], existing_record = None):
    payload = {}
    entry = ""
    existing_record_is_none = existing_record == None
    existing_record_is_blank = existing_record == payload
    existing_record_is_defined = not existing_record_is_none and not existing_record_is_blank

    read_only_fields = [
        'Id',
        'CreatedDate',
        'CreatedById',
        'LastModifiedDate',
        'LastModifiedById'
    ]

    for field_index in range(len(fields)):
        field_name = fields[field_index]
        readonly_field = field_name in read_only_fields
        existing_value = ''
        if existing_record_is_defined and field_name in existing_record:
            existing_value = existing_record[field_name]

        if existing_record_is_blank:
            entry = input(f"  {field_name}: ")
            payload[field_name] = entry
        elif existing_record_is_none and not readonly_field:
            entry = input(f"  {field_name}: ")
            payload[field_name] = entry
        elif existing_record_is_defined and not readonly_field:
            existing_value_caption = existing_value or ''
            if existing_value_caption:
                existing_value_caption = f" [Existing Value = '{existing_value_caption}']"
            entry = input(f"  {field_name}{existing_value_caption}: ") or existing_value
            if entry != existing_value:
                payload[field_name] = entry
    if existing_record_is_none or existing_record_is_defined:
        print("\r\nCheck your values!")
        caption = 'Proceed? (Y)es or (N)o: '
        do_proceed = input(caption)
        while do_proceed.upper() not in ['Y', 'N']:
            reset_entry(caption)
            do_proceed = input(caption)
        if do_proceed.upper() != 'Y':
            return None
    return payload
    

def reset_entry(caption, error_message=None):
    if not error_message:
        error_message = "Invalid Entry"
    sys.stdout.write("\033[F")
    sys.stdout.write("\033[K")
    print(f"{caption}: {error_message}")
    time.sleep(1)
    sys.stdout.write("\033[F")
    sys.stdout.write("\033[K")

def shutdown(iterations):
    if iterations > 0:
        for i in range(iterations+1):
            sys.stdout.write("\r" + "Processing" + "." * i)
            time.sleep(0.2)
            sys.stdout.flush()
        print(" done!")
    print("Goodbye.\r\n")
    time.sleep(0)
    quit()

def animate_msg(msg, iterations=3):
    for i in range(iterations+1):
        sys.stdout.write(f"\r{msg}{'.' * i}")
        time.sleep(0.35)
        sys.stdout.flush()
    sys.stdout.write(f"\r{msg}{'.' * i} ")

def format_get(records, fields=[]):
    formatted_response = f"{len(records)} record(s) discovered:\r\n"
    padding = 20

    for field_index in range(len(fields)):
        if len(fields[field_index]) > padding:
            padding = len(records[record_index]) + 3

    for record_index in range(len(records)):
        record = records[record_index]
        record_value = "  ---\r\n"
        for field_index in range(len(fields)):
            field_name = fields[field_index]
            field_value = record[field_name]
            record_value = "  ".join([record_value,f"{field_name.ljust(padding, '.')} {field_value}\r\n"])
        formatted_response = "".join([formatted_response, f"{record_value}"])
    if len(records) > 0:
        formatted_response = "".join([formatted_response, "  ---\r\n"])
    return formatted_response
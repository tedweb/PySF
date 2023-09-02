
import os, sys, time, math, yaml
from os import path
from dotenv import load_dotenv

source_path = os.path.dirname(os.path.realpath(__file__))
resource_path = os.path.join(source_path, 'resources')

def load_env_vars():
    load_dotenv(path.join(resource_path, '.env'))

def load_config():
    config_file = os.path.join(resource_path, 'config.yml')
    with open(config_file, "r") as yml_file:
        config = yaml.load(yml_file, Loader=yaml.FullLoader)
    return config

def save_config(config):
    config_file = os.path.join(resource_path, "config.yml")
    with open(config_file, 'w') as file:
        yaml.dump(config, file)

def get_selection(listings, caption=None, max_cols=5):
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
        
    result = None
    while result is None:
        entry = input(caption).upper()
        if entry.isnumeric() and int(entry)<len(listings):
            #result = listings[int(entry)-1]
            result = int(entry)-1
        elif entry == 'B':
            result = entry
        elif entry == 'Q':
            shutdown(0)
        else:
            reset_entry(caption)
    return result

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


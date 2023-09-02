import requests

def get(connection, entity, fields=[], search_criteria=None):
    field_string = ','.join(fields)

    try:
        query = f"FIND {{{search_criteria}}} IN ALL FIELDS RETURNING {entity} ({field_string}) WITH METADATA='LABELS' "
        api_path = '/services/data/v54.0/search/'
        params = { 'q':  query }
        response = sf_api_call(connection, api_path, parameters=params)
        return format_get(response, fields)

    except Exception:
        return "Unable to process request due to an API error."

def format_get(response, fields=[]):
    records = response['searchRecords']
    formatted_response = f"{len(records)} record(s) discovered:\r\n"
    padding = 20

    for record_index in range(len(records)):
        if len(records[record_index]) > padding:
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

def sf_api_call(org, action, parameters = {}, method = 'get', data = {}):
    headers = {
        'Content-type': 'application/json',
        'Accept-Encoding': 'gzip',
        'Authorization': 'Bearer %s' % org['authentication']['access_token']
    }
    if method == 'get':
        r = requests.request(method, org['authentication']['instance_url']+action, headers=headers, params=parameters, timeout=30)
    elif method in ['post', 'patch']:
        r = requests.request(method, org['instance_url']+action, headers=headers, json=data, params=parameters, timeout=10)
    else:
        # other methods not implemented in this example
        raise ValueError('Method should be get or post or patch.')
    
    #print('Debug: API %s call: %s' % (method, r.url) )
    if r.status_code < 300:
        if method=='patch':
            return None
        else:
            return r.json()
    else:
        raise Exception(f"API error when calling '{r.url}': '{r.content}")

def get_entity_listing(org):
    entity_names = []
    items = sf_api_call(org, '/services/data/v54.0/sobjects/')
    for index in range(len(items['sobjects'])):
        entity_names.append(items['sobjects'][index]['label'])
    entity_names.sort()
    return entity_names

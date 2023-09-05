import requests
# https://jereze.com/code/authentification-salesforce-rest-api-python/

generic_error = "Unable to process request due to an API error. Check your Salesforce org to ensure proper permission have been granted."

def get(connection, entity_name, id=None, search_criteria=None, fields=[]):
    params = None
    result = {
        'items': [],
        'message': ''
    }

    if id is not None:
        api_path = f"/services/data/v54.0/sobjects/{entity_name}/{id}"
        key = None
    elif search_criteria is not None:
        api_path = '/services/data/v54.0/search/'
        field_string = ','.join(fields)
        query = f"FIND {{{search_criteria}}} IN ALL FIELDS RETURNING {entity_name} ({field_string}) WITH METADATA='LABELS' "
        params = { 'q':  query }
        key = 'searchRecords'

    try:
        response = sf_api_call(connection, api_path, parameters=params)
        if key is not None and key in response:
            result['items'] = response[key]
        else:
            result['items'].append(response)
    except Exception:
        result['message'] = generic_error
    return result

def post(connection, entity_name, payload={}):
    result = {
        'items': [],
        'message': ''
    }

    try:
        api_path = f"/services/data/v40.0/sobjects/{entity_name}/"
        response = sf_api_call(connection, api_path, method="post", data=payload)
        result['items'].append(response)
    except Exception:
        result['message'] = generic_error
    return result

def patch(connection, entity_name, id='', payload={}):
    result = {
        'items': [],
        'message': ''
    }

    try:
        api_path = f"/services/data/v40.0/sobjects/{entity_name}/{id}"
        response = sf_api_call(connection, api_path, method="patch", data=payload)
        result['items'] = response
    except Exception:
        result['message'] = generic_error
    return result


def delete(connection, entity_name, id=''):
    result = {
        'items': [],
        'message': ''
    }

    try:
        api_path = f"/services/data/v40.0/sobjects/{entity_name}/{id}"
        response = sf_api_call(connection, api_path, method="delete")
        result['items'] = response
    except Exception:
        result['message'] = generic_error
    return result

def sf_api_call(org, action, parameters = {}, method = 'get', data = {}):
    headers = {
        'Content-type': 'application/json',
        'Accept-Encoding': 'gzip',
        'Authorization': 'Bearer %s' % org['authentication']['access_token']
    }
    url_path = f"{org['authentication']['instance_url']}{action}"
    if method == 'get':
        r = requests.request(method, url_path, headers=headers, params=parameters, timeout=30)
    elif method in ['post', 'patch']:
        r = requests.request(method, url_path, headers=headers, json=data, params=parameters, timeout=10)
    elif method == 'delete':
        r = requests.request(method, url_path, headers=headers, timeout=10)
    else:
        raise ValueError('Method should be get or post or patch.')
    
    if r.status_code < 300:
        if method=='patch':
            return {
                'id': action[action.rindex('/')+1:],
                'status': r.status_code,
                'data': data
            }
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

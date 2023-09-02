import requests
import json

#instance_url = 'https://tedweb-dev-ed.my.salesforce.com'
#access_token = '0D4W000007RXig!ARcAQNPd2im7vwhgGL86FO5yrreY.RBdSvIFLqE0QN1UwcBOKtt4oCPK58iaL4J66bh40zOrkeB1AIOzclSLlGvt5hYd8wH.'

# def sf_api_call(action, parameters = {}, method = 'get', data = {}):
#     """
#     Helper function to make calls to Salesforce REST API.
#     Parameters: action (the URL), URL params, method (get, post or patch), data for POST/PATCH.
#     """
#     headers = {
#         'Content-type': 'application/json',
#         'Accept-Encoding': 'gzip',
#         'Authorization': 'Bearer %s' % access_token
#     }
#     if method == 'get':
#         r = requests.request(method, instance_url+action, headers=headers, params=parameters, timeout=30)
#     elif method in ['post', 'patch']:
#         r = requests.request(method, instance_url+action, headers=headers, json=data, params=parameters, timeout=10)
#     else:
#         # other methods not implemented in this example
#         raise ValueError('Method should be get or post or patch.')
#     print('Debug: API %s call: %s' % (method, r.url) )
#     if r.status_code < 300:
#         if method=='patch':
#             return None
#         else:
#             return r.json()
#     else:
#         raise Exception('API error when calling %s : %s' % (r.url, r.content))

def get_contact(search_criteria):
    query = "FIND {%s} IN ALL FIELDS RETURNING User (Id, Name, Username) WITH METADATA='LABELS' " % search_criteria
    return sf_api_call('/services/data/v54.0/search/', parameters={
        'q':  query 
    })

def set_contact():
    print("BLA3")

def del_contact():
    print("BLA3")

if __name__ == "__main__":
    result = get_contact("tgodwin\+tedweb@salesforce.com")
    print(json.dumps(result, indent=2))

    #get_contacts()    

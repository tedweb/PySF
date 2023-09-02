import requests
import base64
import json
import asyncio
from aiosfstream import SalesforceStreamingClient


instance_url = 'https://tedweb-dev-ed.my.salesforce.com'
access_token = '00D4W000007RXig!ARcAQBp9zi0nHtzNiMdlUdkGNpUCcQWCciWddXia0p4Fwh79QkKzgXZyAUxsfwWBuMWWFGxRm4Bz23ChJsxzag7lU3_louom'

def sf_api_call(action, parameters = {}, method = 'get', data = {}):
    """
    Helper function to make calls to Salesforce REST API.
    Parameters: action (the URL), URL params, method (get, post or patch), data for POST/PATCH.
    """
    headers = {
        'Content-type': 'application/json',
        'Accept-Encoding': 'gzip',
        'Authorization': 'Bearer %s' % access_token
    }
    if method == 'get':
        r = requests.request(method, instance_url+action, headers=headers, params=parameters, timeout=30)
    elif method in ['post', 'patch']:
        r = requests.request(method, instance_url+action, headers=headers, json=data, params=parameters, timeout=10)
    else:
        # other methods not implemented in this example
        raise ValueError('Method should be get or post or patch.')
    print('Debug: API %s call: %s' % (method, r.url) )
    if r.status_code < 300:
        if method=='patch':
            return None
        else:
            return r.json()
    else:
        raise Exception('API error when calling %s : %s' % (r.url, r.content))

def get_contact(search_criteria):
    query = "FIND {%s} IN ALL FIELDS RETURNING Contact (Id, Name) WITH METADATA='LABELS' " % search_criteria
    return sf_api_call('/services/data/v54.0/search/', parameters={
        'q':  query 
    })

def set_contact():
    print("BLA3")

def del_contact():
    print("BLA3")

async def stream_events():
    # connect to your Salesforce Org (Production or Developer org)
    async with SalesforceStreamingClient(
            consumer_key="3MVG9l2zHsylwlpT_KvMEm4QoV__QiAxFgOjpetFI1Pfel0RvfAkh_LRNU3stc5tcQj2k8GmgTvQEgsKTzXq8",
            consumer_secret="3240914B9AF570D7F0722717FFBF71EF4B4A922F46BD61C16D64ED61CE5C12D0",
            username="tgodwin+tw_pw@salesforce.com",
            password="6v%6BrN2") as client:

        # subscribe to the platform event using CometD
        await client.subscribe("/event/Account_Event__e")

        # listen for incoming messages
        async for message in client:
            topic = message["channel"]
            data = message["data"]
            print(f"{topic}: {data}")


if __name__ == "__main__":
    #result = get_contact("Andy Young")
    #print(json.dumps(result, indent=2))
    #get_contacts()    

    loop = asyncio.get_event_loop()
    loop.run_until_complete(stream_events())
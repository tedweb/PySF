# SalesforceAuthenticator
Requirements:
    VSCode
    Git
    Python 3.8
        pip3
        PyJWT (> python -m pip install pyjwt cryptography requests)
    Salesforce (Dev, Playground, etc)

Key Files:
    .env - This file contains secrets - DO NOT STORE IN A REPO!
    config.yml - This file has the following sections:
        orgs: A list of available Salesforce orgs ready to connect
        authentication: Authentication details to be defined after credentials have been verified.
    util.py - Python script for running utility functions (i.e. loading config file, etc.)
    sf_auth.py - Python script for establishing a connection and access token
    account.py - Python script for accessing the account api
    contact.py - Python script for accessing the contact api

To use, first establish a connection with the following command:
> python3 sf_authenticator/sf_auth.py

This will present a menu of Salesforce orgs to connect to like so:
    Select an org to connect to:
    1: Event Monitoring Analytics
    2: TedWeb-PW
    3: CreativeShark-PW
    4: TedWeb-JWT
    5: Manually enter org details
    Org:

Select and org.  Once selected, connection details will be displayed like below:
    {
        "name": "TedWeb-JWT",
        "status": 200,
        "access_token": "00D4W000007RXig!ARcAQLJg4bOfZnRO0GtzL4PWp2ArN5ZfKJU6wewTxz6VY2p7a1KxyfdwaRrL6cOinAc4bXW0mIafnOabymQoghZo8v7oC6Kj",
        "instance_url": "https://tedweb-dev-ed.my.salesforce.com",
        "id": "https://login.salesforce.com/id/00D4W000007RXigUAG/0054W00000C6LslQAF",
        "token_type": "Bearer",
        "issued_at": null,
        "signature": null
    }

Copy the access token and paste it into either account.py or contact.py.  Then run the following command:
    python3 sf_api/contact.py

Links:
https://jereze.com/code/authentification-salesforce-rest-api-python/

Connections Types:
    Password
    JWT - Be sure login_url is set to 'login.salesforce.com' instead of using custom domain login.

Actions:
    Query objects via REST, SOAP, BULK, GraphQL, etc.
    Listen for events via Pub/Sub API
    Kick off a Flow

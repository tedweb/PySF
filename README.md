# PySF
Requirements:
    VSCode
    Git
    Python 3.8
        pip3
        PyJWT (> python -m pip install pyjwt cryptography requests)
    Salesforce (Dev, Playground, etc)

Key Resource Files:

- config.yml - This is a configuration file that contains a list of available Salesforce orgs ready to connect. Update the 'login_url' attribute to reflext your own org. You can have multiple orgs defined in this file.
Special Note: This file will reference credentials stored in the /resource/.env file (see below).

- .env - This file contains secrets about your credentials.  This .env file included with this repository is simply a template.  Update this file with your own information.
Special Note: DO NOT STORE YOUR ACTUAL .env FILE IN A REPO!

Actions:
    Query objects via REST, SOAP, BULK, GraphQL, etc.
    Listen for events via Pub/Sub API
    Kick off a Flow

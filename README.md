# PySF
This is a simple Python script that connects to a defined Salesforce instance and can perform one or more of the the following actions:
- Query objects via REST, SOAP, BULK, GraphQL, etc.
- Listen for events via Pub/Sub API
- Kick off an automated process such as a Flow or Apex class

### Prerequisites:
- Python 3.8 or higher
- pip3 (`python -m pip3 install --upgrade pip`)
- requests (`pip3 install requests`)
- dotenv (`pip3 install python-dotenv`)
- PyYAML (`pip3 install PyYAML`)
- PyJWT (`python3 -m pip install pyjwt cryptography requests`)

### Configuration:
Open the `/resources/config.yml` file to define one or more Salesforce orgs to connect. Update the 'login_url' attribute to reflect your own org. You can have multiple orgs defined in this file.

**WARNING:** Don't store credential information in this file! Instead, reference this data with necessary environment variables with the defined values stored in the `resources/.env` file. Additionally, exclude this file from any git repositories by including it in your .getignore file.

import asyncio
from aiosfstream import SalesforceStreamingClient

v_eventName = ""

async def stream_events():

    # capture oauth inputs from user
    print()
    print("Welcome to the Platform Event listener from Salesforce4Ever.com!")
    print("****************************************************************")
    print()
    print("Connection to your org will be established using OAUTH2 Username/Password...")
    # init variable here to unsubscribe properly the event in case of exception
 
    v_sandbox = input ("Sandbox? (Y/N): ")
    while v_sandbox != "Y" and v_sandbox != "N":
        print("Wrong value. Enter Y or N") 
        v_sandbox = input ("Sandbox? (Y/N): ")
    if v_sandbox == "Y":
        v_sandbox = True
    else:
        v_sandbox = False

    v_username = input ("Username: ")
    v_password = input ("Password + Security Token: ")
    v_consumer_key = input ("Consumer Key: ")
    v_consumer_secret = input ("Consumer Secret: ")
    v_eventName = input ("Platform Event API Name (e.g. NewEvent__e): ")
    v_ptfevt = "/event/"+v_eventName

    # connect to the org
    async with SalesforceStreamingClient(
            consumer_key=v_consumer_key, 
            consumer_secret=v_consumer_secret, 
            username=v_username, 
            password=v_password, 
            sandbox=v_sandbox) as client:

    # subscribe to topics
        print("Connexion successful to the org!")
        print("Subscribing to the Platform Event...")
        await client.subscribe(v_ptfevt)

        print("Subscribed successfully to the event!")
        print("Listening for incoming messages...")
        # listen for incoming messages
        async for message in client:
            topic = message["channel"]
            data = message["data"]
            payload = message["data"]["payload"]
            print(f"Payload is: {payload}")
            
if __name__ == "__main__":
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(stream_events())
    except KeyboardInterrupt:
        print()
        print()
        print("...Stopping the listener...")
        if v_eventName != "":
            client.unsubscribe(v_ptfevt)
        print("*************************************************************")
        print("Thanks for using our Platform Event listener, enjoy your day!")
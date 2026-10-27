import asyncio
from websockets.asyncio.server import serve
from websockets.exceptions import ConnectionClosedOK
import json
from gpiozero import LED
from time import sleep


CLIENTS = set()

previousChat = []

led = LED(26)

async def broadcastMessage(data):
    message = ""
    if("name" in data) :
        message = data["name"] + ": "
    else :
        message = "Anonymous User: "
    message = message + data["message"]
    response = {"message": message}

    # append response to previous chat
    previousChat.append(response)

    for websocket in CLIENTS.copy():
        try:
            await websocket.send(json.dumps(response))
        except ConnectionClosedOK:
            pass


async def broadcastNewClients(data,newClientId):
    # create response message (someone has joined the chat)
    oldClientMessage = data["name"] + " has joined the chat"
    newClientMessage = "welcome to the chat, " + data["name"]

    # loop through clientsdata["name"] 
    for websocket in CLIENTS.copy():
        # if websocket.id = current client -> do nothing
        if(websocket.id == newClientId):
            await websocket.send(json.dumps({"message" : newClientMessage}))
        else: # if websocket.id = old client -> new user message
            try:
                await websocket.send(json.dumps({"message" : oldClientMessage}))
            except ConnectionClosedOK:
                pass


async def handler(websocket):
    # before anything send previous chats to this client
    await websocket.send(json.dumps(previousChat))

    CLIENTS.add(websocket)
    async for data in websocket:
        data = json.loads(data)
        
        if("message" in data) :
            await broadcastMessage(data)
            continue
        
        if("name" in data) :
            await broadcastNewClients(data, websocket.id) # call new user function
            
        if("led" in data) :
            if(data["led"] == "toggle"):
                led.toggle()

async def main():
    print("Starting websocket server...")
    server = await serve(handler, "", 8001)
    print("Awaiting connection")
    await server.serve_forever()

asyncio.run(main())
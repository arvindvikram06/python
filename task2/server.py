import asyncio
import json
import websockets
from database import init_db, get_rooms, create_room, save_message, get_messages, get_private_messages

# all connected clients are stored here
connected_clients = {}

async def broadcast(message, room=None):
    for ws, info in connected_clients.items():
        if room is None or info.get("room") == room: #common brodcast or specific room
            try:
                await ws.send(json.dumps(message))
            except Exception as e:
                print(f"Error sending message: {e}")



async def send_private(message, room, target_username):
    sender = message.get("sender")
    for ws, info in connected_clients.items():
        if info.get("room") == room and info.get("username") in (target_username, sender): # send private message to target user and sender
            try:
                await ws.send(json.dumps(message))
            except Exception:
                pass

async def notify_users_in_room(room):
    if not room:
        return
    users = []
    for ws, info in connected_clients.items():
        if info.get("room") == room:
            users.append(info["username"])
    
    message = {
        "type": "user_list",
        "users": users
    }
    await broadcast(message, room=room)  



async def handle_set_username(websocket, data):
    username = data.get("username")
    connected_clients[websocket]["username"] = username
    print(f"[USER] {username} connected")
    

    await websocket.send(json.dumps({ # send all rooms to the client
        "type": "room_list",
        "rooms": get_rooms()
    }))

async def handle_create_room(data):
    room_name = data.get("room")
    if create_room(room_name):
        print(f"[ROOM] New room created: {room_name}")
        await broadcast({
            "type": "room_list",
            "rooms": get_rooms() 
        })

async def handle_join(websocket, data):
    room_name = data.get("room")
    old_room = connected_clients[websocket].get("room")
    
    connected_clients[websocket]["room"] = room_name # update the room of the client
    
    if old_room:
        await notify_users_in_room(old_room) # notify users in the old room
    
    print(f"[JOIN] {connected_clients[websocket]['username']} joined #{room_name}")
    
    history = get_messages(room_name)
    await websocket.send(json.dumps({
        "type": "history",
        "messages": history
    }))
    
    await notify_users_in_room(room_name)

async def handle_get_history(websocket, data):
    room_name = connected_clients[websocket].get("room")
    target_user = data.get("target_user")
    
    if room_name:
        if target_user:
            history = get_private_messages(room_name, connected_clients[websocket]["username"], target_user) # get private messages
        else:
            history = get_messages(room_name) # get room messages
            
        await websocket.send(json.dumps({
            "type": "history",
            "messages": history
        }))

async def handle_message(websocket, data):
    room = connected_clients[websocket].get("room")
    sender = connected_clients[websocket].get("username")
    content = data.get("content")
    recipient = data.get("recipient")
    
    if not room or not sender:
        return

    save_message(room, sender, content, recipient)
    
    msg_payload = {
        "type": "message",
        "sender": sender,
        "recipient": recipient,
        "content": content
    }

    if recipient:
        print(f"[PRIVATE] {room} | {sender} -> {recipient}: {content}")
        await send_private(msg_payload, room, recipient)
    else:
        print(f"[ROOM] {room} | {sender}: {content}")
        await broadcast(msg_payload, room=room)


async def handler(websocket):
    connected_clients[websocket] = {"username": None, "room": None}
    
    try:
        async for message in websocket:
            data = json.loads(message)
            action = data.get("action")

            if action == "set_username":
                await handle_set_username(websocket, data)
            elif action == "create_room":
                await handle_create_room(data)
            elif action == "join":
                await handle_join(websocket, data)
            elif action == "get_history":
                await handle_get_history(websocket, data)
            elif action == "message":
                await handle_message(websocket, data)

    except websockets.exceptions.ConnectionClosed: 
        pass
    finally:
        room = connected_clients[websocket].get("room")
        del connected_clients[websocket]
        if room:
            await notify_users_in_room(room)

async def main():
    init_db()
    print("Starting WebSocket server on ws://localhost:8765")
    async with websockets.serve(handler, "localhost", 8765):
        await asyncio.Future()  # run infinitely

if __name__ == "__main__":
    asyncio.run(main())

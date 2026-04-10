from redis_client import r
from config import EVENT_CHANNEL

def publish(msg):
    r.publish(EVENT_CHANNEL, msg)

def listen():
    pubsub = r.pubsub()
    pubsub.subscribe(EVENT_CHANNEL)

    for msg in pubsub.listen():
        if msg["type"] == "message":
            print("[EVENT]", msg["data"])
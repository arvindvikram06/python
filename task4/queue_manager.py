import json,time
from redis_client import r
from config import *

def push_task(task):
    r.rpush(QUEUE_NAME, json.dumps(task))

def pop_task():
    _, data = r.blpop(QUEUE_NAME)
    return json.loads(data)

def push_delayed(task, delay):
    run_at = time.time() + delay
    r.zadd(DELAYED_QUEUE, {json.dumps(task): run_at})

def get_ready_delayed():
    now = time.time()
    tasks = r.zrangebyscore(DELAYED_QUEUE, 0, now)

    for t in tasks:
        r.zrem(DELAYED_QUEUE, t)
        push_task(json.loads(t))

def push_dlq(task):
    r.rpush(DLQ_NAME, json.dumps(task))
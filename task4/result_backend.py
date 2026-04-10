import json
from redis_client import r
from config import RESULT_PREFIX

def store(task):
    r.set(RESULT_PREFIX + task["id"], json.dumps(task))

def get_all():
    keys = r.keys(RESULT_PREFIX + "*")
    return [json.loads(r.get(k)) for k in keys]
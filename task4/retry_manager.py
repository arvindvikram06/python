from config import MAX_RETRIES

def should_retry(task):
    return task["retries"] < MAX_RETRIES

def get_delay(task):
    return 2 ** task["retries"]
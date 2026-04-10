from multiprocessing import Process
import time, json
from queue_manager import *
from tasks import *
from retry_manager import *
from result_backend import store
from event_system import publish

def execute(task):
    func = globals()[task["func"]]
    return func(*task["args"])

def worker(name):
    while True:
        get_ready_delayed()

        task = pop_task()
        print(f"[{name}] Picked {task['id']}")

        task["start_time"] = time.time()

        try:
            result = execute(task)

            task["status"] = "SUCCESS"
            task["result"] = result

            publish(f"{task['id']} SUCCESS")

        except Exception as e:
            task["retries"] += 1

            if should_retry(task):
                delay = get_delay(task)
                push_delayed(task, delay)
                publish(f"{task['id']} RETRY {task['retries']}")
                continue
            else:
                task["status"] = "DEAD"
                push_dlq(task)
                publish(f"{task['id']} DEAD")

        task["end_time"] = time.time()
        store(task)

def start(n=3):
    ps = []
    for i in range(n):
        p = Process(target=worker, args=(f"W{i+1}",))
        p.start()
        ps.append(p)

    for p in ps:
        p.join()

if __name__ == "__main__":
    start()
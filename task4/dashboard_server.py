from result_backend import get_all
import threading
from event_system import listen

def show():
    tasks = get_all()

    print("\n=== Dashboard ===")
    print("+------+--------+--------+--------+---------+")

    for t in tasks:
        duration = "-"
        if t["end_time"] and t["start_time"]:
            duration = round(t["end_time"] - t["start_time"], 2)

        print(f"{t['id']} | {t['func']} | {t['status']} | {t['retries']} | {duration}")

def cli():
    while True:
        cmd = input(">> ")

        if cmd == "check":
            show()

if __name__ == "__main__":
    threading.Thread(target=listen, daemon=True).start()
    cli()
import csv
import os
from datetime import datetime
from tabulate import tabulate   

def generate_report(changes):
    today = datetime.now().strftime("%Y-%m-%d")
    os.makedirs("reports", exist_ok=True)
    path = f"reports/{today}.csv"

    table = []

    for title, old_price, new_price in changes:
        change = round(new_price - old_price, 2)
        percent_change = round(((new_price - old_price) / old_price) * 100, 2)
        table.append([title, old_price, new_price, change, percent_change])

    with open(path, "w", newline="") as f: 
        writer = csv.writer(f)
        writer.writerow(["Product", "Old Price", "New Price", "Change", "Change (%)"])
        writer.writerows(table)

    print("\nPrice Change Report:\n") 
    print(tabulate( # used tabulate library for command line output
        table,
        headers=["Product", "Old Price", "New Price", "Change", "Change (%)"],
        tablefmt="grid"
    ))

    print(f"\n{len(table)} changes saved to {path}")
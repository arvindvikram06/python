import schedule
import time
import asyncio


from scraper import main  

def job():
    print("Running scraper at 3:00 AM...")
    asyncio.run(main())


schedule.every().day.at("03:00").do(job)

print("Scheduler started for every 3:00 AM")

while True:
    schedule.run_pending()
    time.sleep(60)
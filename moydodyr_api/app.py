#!/usr/bin/env python3
from typing import Union
from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler
from els_scraper.runner import main_run

app = FastAPI()

job_defaults = {
    'coalesce': False,
}
scheduler = BackgroundScheduler(job_defaults)

def periodic_task():
    print('pointcut=[BEFORE] els scraper')
    result = main_run()
    print(f"pointcut=[AFTER] result {result}")
    # print("Running periodic task")

# Start the scheduler and add the periodic task
# scheduler.add_job(periodic_task, 'interval', seconds=60)
scheduler.add_job(periodic_task, 'cron', minute='*/7', hour='6-22')
# scheduler.add_job(periodic_task, 'cron', minute='*/30', hour='22-6')
scheduler.start()


def write_notification(email: str, message=""):
    with open("log.txt", mode="w") as email_file:
        content = f"notification for {email}: {message}"
        email_file.write(content)


@app.post("/send-notification/{email}")
async def send_notification(email: str):
    # background_tasks.add_task(write_notification, email, message="some notification")
    return {"message": "Notificatidddddddon sent in the background"}
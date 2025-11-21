import schedule
import time
import threading
from scraper.odds_scraper import collect_events
from pipeline.quantum_pipeline_v7 import generate_daily_tips

def job_single_kombi():
    events = collect_events()
    tips = generate_daily_tips(events)
    print("Daily tips generated:", tips)

def job_live():
    events = collect_events()
    live_events = [e for e in events if e.get("live")]
    print("Live check:", len(live_events))

def start_scheduler():
    schedule.every().day.at("09:00").do(job_single_kombi)
    schedule.every().hour.do(job_live)

    def run():
        while True:
            schedule.run_pending()
            time.sleep(1)

    thread = threading.Thread(target=run, daemon=True)
    thread.start()

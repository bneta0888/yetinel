from fastapi import APIRouter
from ..detection import run_all_detections
from apscheduler.schedulers.background import BackgroundScheduler
from contextlib import asynccontextmanager


router = APIRouter()

# Define the lifespan (Startup/Shutdown logic)
@asynccontextmanager
async def lifespan(app):
    # This runs when the server starts
    print("Starting background detection scheduler...")
    scheduler = BackgroundScheduler()

    # Add the job : run every 2 minutes
    scheduler.add_job(run_all_detections, 'interval', minutes=2)

    # Run once immediately on startup so we dont wait 2 mins
    run_all_detections()

    scheduler.start()

    yield

    # This runs when the server is stopped
    print("Shutting down the scheduler...")
    scheduler.shutdown()

@router.post("/detect/run_detection")
def run_detection():
    run_all_detections()
    return {"status": "detection run"}

from fastapi import APIRouter, BackgroundTasks
from threading import Event
from app.utils.scraper import run_scraper

router = APIRouter()

# Global Event to control scraper execution
stop_event = Event()

@router.get("/start", tags=["Scraper"])
def start_scraper(background_tasks: BackgroundTasks):
    """Manually start the scraper."""
    if stop_event.is_set():
        stop_event.clear()  # Reset stop event if previously set
    background_tasks.add_task(run_scraper, stop_event)
    return {"message": "Scraper started in the background."}

@router.get("/stop", tags=["Scraper"])
def stop_scraper():
    """Stop the running scraper."""
    stop_event.set()  # Signal the scraper to stop
    return {"message": "Scraper stop signal sent."}

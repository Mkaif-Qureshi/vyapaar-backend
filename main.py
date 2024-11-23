from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.background import BackgroundScheduler
from app.utils.scraper import run_scraper
from app.routes.scraper_routes import router as scraper_router
from app.auth.auth_routes import router as auth_router
from app.routes.user_routes import router as user_router
from app.routes.analytics_routes import router as analytics_router
from app.routes.chatbot_routes import router as chatbot_router
from app.routes.compliance_routes import router as compliance_router
from app.routes.document_routes import router as document_router
from app.routes.incentive_routes import router as incentive_router
from app.routes.risk_routes import router as risk_router

app = FastAPI(title="My Application", version="1.0.0", description="An API for user management and more.")
from app.routes.user_routes import router as user_router  # Ensure this is a FastAPI router

# Configure the scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(func=run_scraper, trigger="cron", hour=0)  # Run at midnight
scheduler.start()

# Create FastAPI instance
app = FastAPI(
    title="My Application",
    version="1.0.0",
    description="An Vyapaar API"
)

# CORS Middleware
# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_origins=["*"],  # Change for specific domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(user_router, prefix="/users", tags=["Users"])
app.include_router(analytics_router, prefix="/analytics", tags=["Analytics"])
app.include_router(chatbot_router, prefix="/chatbot", tags=["Chatbot"])
app.include_router(compliance_router, prefix="/compliance", tags=["Compliance"])
app.include_router(document_router, prefix="/documents", tags=["Documents"])
app.include_router(incentive_router, prefix="/incentives", tags=["Incentives"])
app.include_router(risk_router, prefix="/risks", tags=["Risks"])

app.include_router(scraper_router, prefix="/scraper", tags=["Scraper"])

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Welcome to the API!"}

@app.on_event("shutdown")
def shutdown_event():
    scheduler.shutdown()

# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

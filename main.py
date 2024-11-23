from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.auth.auth_routes import router as auth_router
from app.routes.user_routes import router as user_router  # Ensure this is a FastAPI router

# Create FastAPI instance
app = FastAPI(title="My Application", version="1.0.0", description="An API for user management and authentication.")

# CORS Middleware (if needed for frontend/backend integration)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to specific domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(user_router, prefix="/users", tags=["Users"])

# Root route for health check or default response
@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Welcome to the API!"}

# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)


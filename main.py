from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.auth.auth_routes import router as auth_router
from app.routes.user_routes import router as user_router
from app.routes.analytics_routes import router as analytics_router
from app.routes.chatbot_routes import router as chatbot_router
from app.routes.compliance_routes import router as compliance_router
from app.routes.document_routes import router as document_router
from app.routes.incentive_routes import router as incentive_router
from app.routes.risk_routes import router as risk_router
# from app.routes.document_routes import get_mistral_data , call_mistral_api

app = FastAPI(title="My Application", version="1.0.0", description="An API for user management and more.")

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(user_router, prefix="/users", tags=["Users"])
app.include_router(analytics_router, prefix="/analytics", tags=["Analytics"])
app.include_router(chatbot_router, prefix="/chatbot", tags=["Chatbot"])
app.include_router(compliance_router, prefix="/compliance", tags=["Compliance"])
app.include_router(document_router, prefix="/documents", tags=["Documents"])
app.include_router(incentive_router, prefix="/incentives", tags=["Incentives"])
app.include_router(risk_router, prefix="/risks", tags=["Risks"])
# app.include_router(document_router, prefix="/call-mistral", tags=["Mistral_resposne"])
# app.include_router(document_router, prefix="/call-mistral", tags=["Mistral_resposne"])

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Welcome to the API!"}

# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

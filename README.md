# Vyapaar Backend

**Vyapaar Backend** is the server-side application of the Vyapaar platform. Built with **FastAPI**, it handles authentication, product management, trade transactions, and integration with the frontend to provide real-time data and insights for exporters.

## Features
- **Authentication**: Secure user registration and login with JWT tokens.
- **Product Management**: API to add, update, and delete products.
- **Trade Management**: Manage trade records through RESTful API endpoints.
- **News Integration**: Provides the latest business news.
- **FastAPI**: High-performance web framework for building APIs.

## Tech Stack
- **Backend Framework**: FastAPI (Python)
- **Authentication**: JWT for secure user sessions.
- **Database**: PostgreSQL (Supabase) for storing product and trade data.
- **API Documentation**: Auto-generated with FastAPI's built-in Swagger UI.
- **Data Aggregation**: External APIs for trade-related insights.
- **Security**: HTTPS (SSL/TLS), JWT for authentication.

## Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/Mkaif-Qureshi/vyapaar-backend.git
   ```
2. Navigate to the project folder:
   ```bash
   cd vyapaar-backend
   ```
4. Create a virtual environment (optional but recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
6. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
8. Run the FastAPI server:
   ```bash
   uvicorn app:app --reload
   ```
10. Access API Documentation:

FastAPI provides automatic interactive API documentation via Swagger UI at:
   ```bash
   http://localhost:8000/docs
   ```

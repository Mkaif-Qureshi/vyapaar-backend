from fastapi import APIRouter, UploadFile, File
import httpx
from fastapi import HTTPException

router = APIRouter()
MISTRAL_API_BASE_URL = "https://api.mistral.com/v1"

# Replace with your Mistral API key if needed
MISTRAL_API_KEY = "your_mistral_api_key"


@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """
    Endpoint to upload a document.
    """
    return {"filename": file.filename, "message": "Document uploaded successfully"}

@router.get("/{document_id}")
def get_document(document_id: int):
    """
    Endpoint to fetch a specific document by ID.
    """
    return {"message": f"Document {document_id} retrieved successfully"}



"""
create a route to send llm response to the frontend from the backend
the mistral api
"""

@router.post("/call-mistral")
async def call_mistral_api(payload: dict):
    """
    Route to call the Mistral API with a POST request and send the response to the frontend.
    :param payload: The request payload from the frontend (JSON format).
    :return: The response from the Mistral API.
    """
    url = f"{MISTRAL_API_BASE_URL}/endpoint"  # Update with the correct endpoint
    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json",
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, headers=headers)
            response.raise_for_status()  # Raise an HTTPException for non-2xx responses

            # Send the response back to the frontend
            return response.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/call-mistral")
async def get_mistral_data(query_params: dict = None):
    """
    Route to call the Mistral API with a GET request and send the response to the frontend.
    :param query_params: The query parameters from the frontend (optional).
    :return: The response from the Mistral API.
    """
    url = f"{MISTRAL_API_BASE_URL}/data"  # Update with the correct endpoint
    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=query_params, headers=headers)
            response.raise_for_status()

            # Send the response back to the frontend
            return response.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

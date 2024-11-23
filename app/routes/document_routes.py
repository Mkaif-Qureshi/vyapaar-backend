from fastapi import APIRouter, UploadFile, File

router = APIRouter()

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

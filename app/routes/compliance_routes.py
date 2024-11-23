from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_compliance_info():
    """
    Endpoint to fetch compliance-related information.
    """
    return {"message": "Compliance information retrieved successfully"}

@router.post("/")
def create_compliance_record(data: dict):
    """
    Endpoint to create a new compliance record.
    """
    return {"message": "Compliance record created successfully", "data": data}

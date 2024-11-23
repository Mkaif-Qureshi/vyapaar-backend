from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def list_incentives():
    """
    Endpoint to list all incentives.
    """
    return {"message": "Incentives retrieved successfully"}

@router.post("/")
def create_incentive(data: dict):
    """
    Endpoint to create a new incentive.
    """
    return {"message": "Incentive created successfully", "data": data}

from fastapi import APIRouter

router = APIRouter()

@router.post("/chat")
def chatbot_response(user_input: str):
    """
    Endpoint to get a chatbot response based on user input.
    """
    # Stubbed response for demonstration
    response = f"Chatbot response to: {user_input}"
    return {"response": response}

from fastapi import APIRouter, UploadFile, File, HTTPException
import httpx
from langchain.prompts import PromptTemplate
from langchain.schema import SystemMessage, HumanMessage
from langchain_mistralai import ChatMistralAI
import os 
from dotenv import load_dotenv

load_dotenv()
router = APIRouter()
MISTRAL_API_BASE_URL = "https://api.mistral.com/v1"

# Replace with your Mistral API key if needed
MISTRAL_API_KEY = '4BAZ7bsmxSS0bCh6Z0GLCgPD9kNAJDG1'

# Initialize LLM
llm = ChatMistralAI(
    model="mistral-large-latest",
    temperature=0.3,
)

# Define system message for the LLM
system_message = SystemMessage(
    content=(
        "You are Vyapaar, an expert in international trade and eco-friendly packaging. "
        "Your role is to provide detailed, well-researched, and optimized answers about "
        "export compliance, documentation, risk analysis, and business expansion for eco-friendly product manufacturers."
    )
)

# Define prompt template
prompt_template = PromptTemplate(
    input_variables=["user_input", "context"],
    template=(
        "User input:\n\n{user_input}\n\n"
        "Context information:\n\n{context}\n\n"
        "Generate a clear, actionable, and detailed response for an exporter."
    )
)

@router.post("/call-mistral")
async def call_mistral_api(payload: dict):
    """
    Route to call the Mistral API with a POST request using a generated prompt and return the response to the frontend.
    :param payload: The request payload from the frontend, including user input and context.
    :return: The response from the LLM.
    """
    user_input = payload.get("user_input", "")
    context = payload.get("context", "")

    # Build the prompt using the template
    prompt = prompt_template.format(
        user_input=user_input,
        context=context
    )

    # Prepare the request for the Mistral API
    url = f"{MISTRAL_API_BASE_URL}/endpoint"  # Update with the correct endpoint
    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json",
    }

    try:
        # Generate the response using the LLM
        messages = [system_message, HumanMessage(content=prompt)]
        llm_response = llm(messages)

        # Simulate the API call
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json={"prompt": prompt}, headers=headers)
            response.raise_for_status()  # Raise an exception for HTTP errors

        # Return the LLM response to the frontend
        return {"llm_response": llm_response.content, "api_response": response.json()}
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

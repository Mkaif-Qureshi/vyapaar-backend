from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from langchain.prompts import PromptTemplate
from langchain.schema import SystemMessage, HumanMessage
from langchain_mistralai import ChatMistralAI
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
import os

# Initialize embedding function (same as used for creating the vector store)
embedding_function = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Initialize router
router = APIRouter()


# Absolute path to the Chroma DB folder
persist_directory = os.path.join(os.path.dirname(__file__), "../chroma_db")

# Initialize Chroma with embedding function for retrieval
vectorstore = Chroma(persist_directory=persist_directory, embedding_function=embedding_function)
retriever = vectorstore.as_retriever()


# vectorstore = Chroma(persist_directory=persist_directory)
# # vectorstore = Chroma(persist_directory="../chroma_db")
# retriever = vectorstore.as_retriever()

# Initialize LLM
llm = ChatMistralAI(
    model="mistral-large-latest",
    temperature=0.3,
)

# Define system message for chatbot behavior
system_message = SystemMessage(
    content=(
        "You are Vyapaar, an expert in international trade and eco-friendly packaging. Your role is to provide "
        "detailed, well-researched, and optimized answers about export compliance, documentation, risk analysis, and "
        "business expansion for eco-friendly product manufacturers like GreenPulse."
    )
)

# Define prompt template
prompt_template = PromptTemplate(
    input_variables=["retrieved_documents", "user_query"],
    template=(
        "You have access to the following retrieved information:\n\n"
        "{retrieved_documents}\n\n"
        "The user asked the following question:\n\n"
        "{user_query}\n\n"
        "Provide a detailed and comprehensive answer tailored for an exporter. Include actionable insights, compliance "
        "guidelines, documentation advice, and any relevant eco-friendly packaging incentives. Make your response clear, "
        "structured, and user-friendly."
    )
)

# Request schema for incoming queries
class QueryRequest(BaseModel):
    query: str

# Response schema
class QueryResponse(BaseModel):
    response: str

# API endpoint for chatbot query
@router.post("/chatbot", response_model=QueryResponse)
async def chatbot_query(request: QueryRequest):
    query = request.query
    
    try:
        # Retrieve documents based on the query
        retrieved_docs = retriever.get_relevant_documents(query)
        retrieved_text = "\n".join([doc.page_content for doc in retrieved_docs])

        # Construct the prompt
        prompt = prompt_template.format(
            retrieved_documents=retrieved_text,
            user_query=query
        )

        # Generate the response using the LLM
        messages = [system_message, HumanMessage(content=prompt)]
        response = llm(messages)

        return QueryResponse(response=response.content)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

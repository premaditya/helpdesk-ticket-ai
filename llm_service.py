from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from pydantic import BaseModel, Field

from prompts import helpdesk_prompt

load_dotenv()

class HelpdeskTicket(BaseModel):
    category: str = Field(
        description = "The category of the support ticket"
    )

    priority: str = Field(
        description = "The priority level of the support ticket"
    )

    summary: str = Field(
        description = "A short summary of the support issue"
    )

    suggested_action: str = Field(
            description = "The recommended next action for resolving the issue"
    )


llm = ChatGoogleGenerativeAI(
    model = "gemini-3.6-flash",
    temperature = 0.5
)

structured_llm = llm.with_structured_output(HelpdeskTicket)

helpdesk_chain = helpdesk_prompt | structured_llm


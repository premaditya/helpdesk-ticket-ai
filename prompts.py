from langchain_core.prompts import ChatPromptTemplate

helpdesk_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """Analyze the IT support ticket.

Classify it into exactly one category:
Hardware, Software, Network, Account, Security, or Other.

Classify its priority as exactly one:
Low, Medium, High, or Critical.

Also provide:
- a concise problem summary
- one appropriate next action

Use only information supported by the ticket. Do not invent details."""
    ),
    (
        "human",
        "Support ticket\n{ticket}"
    )
])
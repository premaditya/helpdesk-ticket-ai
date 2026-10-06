# 🛠️ AI IT Helpdesk

An AI-powered IT support ticket analyzer built with **LangChain**, **Google Gemini**, **Streamlit**, and **LangSmith**. Paste in a support ticket and the app returns a structured analysis: category, priority, summary, and a recommended next action. It also shows per-request observability metrics pulled from LangSmith.

## ✨ Features

- **Ticket classification** into one of: Hardware, Software, Network, Account, Security, or Other
- **Priority assignment**: Low, Medium, High, or Critical
- **Concise issue summary** based only on the ticket's content
- **Suggested next action** for resolving the issue
- **Structured output** via Pydantic models and `with_structured_output`
- **LangSmith tracing** with a live metrics panel showing:
  - App latency
  - Input, output, and total tokens
  - Estimated cost
  - LLM latency
- **Custom dark-themed UI** built with Streamlit and custom CSS

## 🧱 Tech Stack

| Layer | Technology |
|---|---|
| UI | Streamlit |
| LLM framework | LangChain |
| Model | Google Gemini (`langchain-google-genai`) |
| Observability | LangSmith |
| Data validation | Pydantic |
| Config | python-dotenv |

## 📁 Project Structure

```
helpdesk-ticket-ai/
├── app.py              # Streamlit UI, ticket analysis flow, LangSmith metrics
├── llm_service.py      # Gemini model, Pydantic schema, and helpdesk chain
├── prompts.py          # System and human prompt templates
├── requirements.txt    # Python dependencies
├── .env                # API keys and config (not committed)
└── README.md
```

## ⚙️ How It Works

1. The user enters a support ticket in the Streamlit app.
2. `helpdesk_chain` (prompt → Gemini with structured output) analyzes the ticket.
3. The model returns a validated `HelpdeskTicket` object with `category`, `priority`, `summary`, and `suggested_action`.
4. The app renders the results as cards.
5. After a short delay, the app queries LangSmith for the latest `Helpdesk Ticket Request` trace and displays token usage, cost, and latency.

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/premaditya/helpdesk-ticket-ai
cd helpdesk-ticket-ai
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
# Google Gemini
GOOGLE_API_KEY=your_google_api_key

# LangSmith
LANGSMITH_TRACING=true
LANGSMITH_API_KEY=your_langsmith_api_key
LANGSMITH_PROJECT=your_project_name
```

- Get a Gemini API key from [Google AI Studio](https://aistudio.google.com/).
- Get a LangSmith API key from [LangSmith](https://smith.langchain.com/).

### 5. Run the app

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`.

## 🧪 Example

**Input ticket**

```
My laptop suddenly shuts down whenever I connect the external monitor.
```

**Sample output**

| Field | Result |
|---|---|
| Category | Hardware |
| Priority | Medium |
| Summary | Laptop shuts down when an external monitor is connected. |
| Suggested action | Test with a different cable/monitor and check power adapter and graphics drivers. |

*(Actual output varies by model response.)*

## 📊 Observability with LangSmith

Each request is traced under the run name **Helpdesk Ticket Request**. In the LangSmith dashboard you can inspect:

- The full prompt sent to the model
- The structured response
- Token usage and estimated cost
- Latency for each step of the chain

## 🛠️ Customization

- **Change the model or temperature:** edit `llm_service.py`
- **Adjust categories, priorities, or instructions:** edit `prompts.py`
- **Add or remove output fields:** update the `HelpdeskTicket` model in `llm_service.py` and render the new field in `app.py`

## ⚠️ Notes

- LangSmith metrics may take a couple of seconds to appear because traces are processed asynchronously. If they aren't ready, the app shows a friendly message instead of failing.
- Never commit your `.env` file. Add it to `.gitignore`.

## 📄 License

This project is for educational purposes. Add a license of your choice here.
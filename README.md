# AI Customer Support Agent

An AI-powered customer support application built with Python, LangChain, Ollama, and FAISS. The project combines retrieval-augmented generation (RAG), order lookup tools, conversation history, and simulated human-support escalation.

## Problem Statement

Traditional customer support systems often require customers to search through FAQs or wait for a support representative. This project explores how a local language model can answer common customer questions using company information, retrieve sample order details, and record issues that require human follow-up.

## Features

- **AI chatbot:** Uses the Qwen 2.5 3B model through Ollama.
- **Knowledge base:** Reads company policies from a local FAQ file.
- **RAG:** Splits documents into chunks, generates embeddings, and retrieves relevant information using FAISS.
- **Order lookup:** Checks sample order records using an order ID.
- **Conversation memory:** Uses messages from the current session to understand follow-up questions.
- **Human-support escalation:** Records unresolved issues in a local text file.
- **Automated tests:** Tests order lookup and escalation behavior.

## Technologies Used

- Python
- LangChain
- LangChain Community
- Ollama
- Qwen 2.5 3B
- Nomic Embed Text
- FAISS
- Python unittest

## Project Architecture

1. The customer enters a question.
2. The agent receives the conversation history.
3. The language model decides whether to answer directly or request a tool.
4. The FAQ tool retrieves relevant company information, or the order tool looks up sample order details.
5. The escalation tool can record an issue requiring human follow-up.
6. Tool results are returned to the language model to generate a response.

## Project Structure

```text
AI-Customer-Support-Agent/
├── data/
│   └── faq.txt
├── app.py
├── rag.py
├── orders.py
├── support.py
├── agent.py
├── test_day6.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Requirements

- Python 3.12
- Ollama installed and running
- Qwen 2.5 3B model
- Nomic Embed Text embedding model
- Python dependencies listed in `requirements.txt`

## Installation and Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd AI-Customer-Support-Agent
```

Replace `YOUR_GITHUB_REPOSITORY_URL` with your actual repository URL.

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Download the Ollama models

```bash
ollama pull qwen2.5:3b
ollama pull nomic-embed-text
```

Ensure Ollama is running before starting the application.

### 5. Run the application

```bash
python agent.py
```

Type `exit` to end the conversation.

## Running Tests

Run the automated tests with:

```bash
python -m unittest test_day6 -v
```

## Sample Test Scenarios

| Customer question | Expected behavior |
|---|---|
| How long does delivery take? | Retrieves the delivery policy |
| Where is my order TS1001? | Looks up the sample order |
| What product did I order? | Uses conversation history where available |
| Where is my order TS9999? | Reports that the order was not found |
| I need human assistance | May record an escalation ticket |
| Do you sell gaming chairs? | Should not invent unsupported company information |

## Limitations

- Order information is stored in a demonstration database, not a real e-commerce system.
- Escalation tickets are recorded locally; no real support employee is notified.
- Conversation history is not persistent across application restarts.
- The application depends on local Ollama models and available system resources.
- Model responses and retrieval results require further evaluation before production use.
- Authentication, customer privacy controls, and a real ticket-management integration are not implemented.

## Future Improvements

- Build a web interface using Streamlit or FastAPI.
- Integrate a real order-management API.
- Add persistent conversation memory.
- Use LangGraph for explicit agent workflow management.
- Add customer authentication and access controls.
- Improve retrieval evaluation and response validation.
- Integrate a real human-support ticketing system.

## Learning Outcomes

This project demonstrates practical experience with local LLMs, prompt engineering, RAG, vector search, tool calling, conversation history, Python testing, and project documentation.

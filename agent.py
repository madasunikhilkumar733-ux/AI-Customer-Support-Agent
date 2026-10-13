
from pathlib import Path

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_core.tools import tool
from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
    ToolMessage,
)

from orders import check_order
from support import create_support_ticket


# -----------------------------------------
# 1. Find the project folder
# -----------------------------------------

PROJECT_DIR = Path(__file__).resolve().parent
FAQ_PATH = PROJECT_DIR / "data" / "faq.txt"


# -----------------------------------------
# 2. Load the FAQ and build the RAG system
# -----------------------------------------

loader = TextLoader(str(FAQ_PATH), encoding="utf-8")
documents = loader.load()

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
)

chunks = splitter.split_documents(documents)

embeddings = OllamaEmbeddings(model="nomic-embed-text")

vector_store = FAISS.from_documents(chunks, embeddings)

retriever = vector_store.as_retriever(
    search_kwargs={"k": 3}
)


# -----------------------------------------
# 3. Define the tools
# -----------------------------------------

@tool
def search_company_information(query: str) -> str:
    """Search TechShop policies about delivery, returns,
    refunds, payments, and other company FAQ information."""

    results = retriever.invoke(query)

    if not results:
        return "No relevant company information was found."

    return "\n\n".join(
        doc.page_content for doc in results
    )


@tool
def order_status(order_id: str) -> str:
    """Look up the status of an order using its order ID."""

    return check_order(order_id)


@tool
def escalate_to_human(issue: str, order_id: str = "Not provided") -> str:
    """Record a customer complaint or unresolved issue
    for human support follow-up."""

    return create_support_ticket(issue, order_id)


tools = [
    search_company_information,
    order_status,
    escalate_to_human,
]

tool_map = {item.name: item for item in tools}


# -----------------------------------------
# 4. Create the AI model
# -----------------------------------------

model = ChatOllama(
    model="qwen2.5:3b",
    temperature=0,
)

model_with_tools = model.bind_tools(tools)


# -----------------------------------------
# 5. Start conversation memory
# -----------------------------------------

history = [
    SystemMessage(
        content="""
You are a polite and professional TechShop customer support agent.

Rules:
1. Use search_company_information for company policies and FAQs.
2. Use order_status when a customer asks about a specific order.
3. Use escalate_to_human when the issue cannot be resolved safely,
   or when the customer needs human assistance.
4. Never invent order details, refund approvals, or company policies.
5. If you do not know the answer, explain that clearly.
6. Use earlier messages to understand follow-up questions.
7. Never claim a human was notified unless that actually happened.
8. Do not reveal private information about another customer's order.
"""
    )
]


# -----------------------------------------
# 6. Process one customer question
# -----------------------------------------

def answer_customer(question: str) -> str:
    history.append(HumanMessage(content=question))

    # Allow several tool calls in one turn, with a safety limit.
    for _ in range(5):
        response = model_with_tools.invoke(history)

        # Remember the AI response, including any tool requests.
        history.append(response)

        # No tool requested: this is the final answer.
        if not response.tool_calls:
            return str(response.content)

        # Execute the tools requested by the model.
        for tool_call in response.tool_calls:
            name = tool_call["name"]
            arguments = tool_call["args"]
            call_id = tool_call["id"]

            selected_tool = tool_map.get(name)

            if selected_tool is None:
                result = f"Unknown tool: {name}"
            else:
                try:
                    result = selected_tool.invoke(arguments)
                except Exception as error:
                    print(f"Tool error ({name}): {error}")
                    result = (
                        "The tool failed. Do not invent a result; "
                        "explain the problem to the customer."
                    )

            print(f"\n[Tool used: {name}]")

            history.append(
                ToolMessage(
                    content=str(result),
                    tool_call_id=call_id,
                )
            )

    return (
        "I couldn't complete that request automatically. "
        "Please contact human support for further assistance."
    )


# -----------------------------------------
# 7. Chat loop
# -----------------------------------------

print("=== TechShop AI Customer Support ===")
print("Type 'exit' to stop the conversation.\n")

while True:
    question = input("Customer: ").strip()

    if question.lower() in {"exit", "quit"}:
        print("AI: Thank you for contacting TechShop!")
        break

    if not question:
        continue

    try:
        answer = answer_customer(question)
        print("\nAI Support Agent:", answer, "\n")
    except Exception as error:
        print("\nAn error occurred:", error)
        print("Check your Ollama service, model, and terminal output.\n")

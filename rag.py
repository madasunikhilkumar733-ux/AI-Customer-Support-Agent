from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings, ChatOllama


# -----------------------------------
# 1. Load FAQ
# -----------------------------------

loader = TextLoader(
    "data/faq.txt",
    encoding="utf-8"
)

documents = loader.load()


# -----------------------------------
# 2. Split FAQ into chunks
# -----------------------------------

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

chunks = text_splitter.split_documents(documents)


# -----------------------------------
# 3. Create embeddings
# -----------------------------------

embeddings = OllamaEmbeddings(
    model="nomic-embed-text"
)


# -----------------------------------
# 4. Create FAISS vector database
# -----------------------------------

vector_store = FAISS.from_documents(
    chunks,
    embeddings
)


# -----------------------------------
# 5. Create retriever
# -----------------------------------

retriever = vector_store.as_retriever(
    search_kwargs={"k": 3}
)


# -----------------------------------
# 6. Load LLM
# -----------------------------------

model = ChatOllama(
    model="qwen2.5:3b",
    temperature=0
)


# -----------------------------------
# 7. Ask customer
# -----------------------------------

question = input("Customer: ")


# -----------------------------------
# 8. Retrieve relevant information
# -----------------------------------

results = retriever.invoke(question)


context = "\n\n".join(
    document.page_content
    for document in results
)


# -----------------------------------
# 9. Create prompt
# -----------------------------------

prompt = f"""
You are a professional customer support agent for TechShop.

Answer the customer's question using ONLY the information
provided in the context.

If the answer is not available in the context, say:

"I don't have enough information to answer that.
Please contact human support."

Do not invent information.

CONTEXT:
{context}

CUSTOMER QUESTION:
{question}
"""


# -----------------------------------
# 10. Generate answer
# -----------------------------------

response = model.invoke(prompt)


# -----------------------------------
# 11. Display answer
# -----------------------------------

print("\nAI Support Agent:", response.content)
from langchain_ollama import ChatOllama
llm=ChatOllama(model="qwen2.5:3b",temperature=0.7)

with open("data/faq.txt", "r", encoding="utf-8") as file:
    faq=file.read()

question = input("customer question: ")

prompt = f"""
You are a professional customer support agent for TechShop.

Answer the customer's question using ONLY the company
information provided below.
If the answer is not available in the company information,
say:

"I don't have enough information to answer that.
Please contact human support."

Do not invent policies, prices, delivery times, or other information.

COMPANY INFORMATION:
{faq}
CUSTOMER QUESTION:
{question}
"""
response = llm.invoke(prompt)

print("techshop support agent: ",response.content)
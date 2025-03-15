from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

llm_openai = ChatOpenAI(
    model="gpt-4o-mini-2024-07-18"
)


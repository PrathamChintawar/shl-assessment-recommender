from dotenv import load_dotenv
import os

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

EMBEDDING_MODEL = "all-MiniLM-L6-v2"

TOP_K = 5

LLM_MODEL = "gemini-2.5-flash"
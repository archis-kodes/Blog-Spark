from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv

class GeminiLLM:
    def __init__(self):
        load_dotenv()

    def get_llm(self):
        try:
            os.environ["GEMINI_API_KEY"] = self.gemini_api_key = os.getenv("GEMINI_API_KEY")
            llm = ChatGoogleGenerativeAI(api_key = self.gemini_api_key, model = "gemini-3.5-flash")
            return llm
        except Exception as e:
            raise ValueError('Error occured with Exception : {e}')
import uvicorn
from fastapi import FastAPI, Request
from src.graphs.graph_builder import GraphBuilder
from src.llms.gemini_llm import GeminiLLM
from fastapi.middleware.cors import CORSMiddleware

import os
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

# For Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

os.environ["LANGSMITH_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")

@app.post("/blogs")
async def create_blogs(requests: Request):
    data = await requests.json()
    topic = data.get("topic", " ")

    # Get LLM object
    geminillm = GeminiLLM()
    llm = geminillm.get_llm()

    # Get Graph
    graph_builder =  GraphBuilder(llm)
    if topic:
        graph = graph_builder.setup_graph(usecase = "topic")
        state = graph.invoke({"topic":topic})

    return {"data": state}

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port = 8000, reload = True)
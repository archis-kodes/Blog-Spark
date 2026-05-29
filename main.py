import uvicorn
from fastapi import FastAPI, Request
from src.graphs.graph_builder import GraphBuilder
from src.llms.groq_llm import GroqLLM
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
    groqllm = GroqLLM()
    llm = groqllm.get_llm()

    # Get Graph
    graph_builder = GraphBuilder(llm)
    if topic:
        graph = graph_builder.setup_graph(usecase="topic")
        state = graph.invoke({"topic": topic})

    blog = state["blog"]
    images = state.get("images", [])

    # Distribute images across content
    paragraphs = blog["content"].split("\n\n")
    total = len(paragraphs)
    interval = max(1, total // (len(images) + 1))

    for i, img in enumerate(images):
        insert_at = min(interval * (i + 1), len(paragraphs) - 1)
        image_md = f"![{img['alt']}]({img['url']})\n*Photo by {img['credit']}*"
        paragraphs.insert(insert_at, image_md)

    full_content = "\n\n".join(paragraphs)

    return {
        "data": {
            "title": blog["title"],
            "content": full_content,
            "images": images
        }
    }

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
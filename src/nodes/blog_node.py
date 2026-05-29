import requests
import os

from src.states.blogstate import BlogState

def extract_text(content):
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "".join(
            block["text"] if isinstance(block, dict) else str(block) for block in content if not isinstance(block, dict) or block.get("type") == "text"
        )
    return str(content)

class BlogNode:
    """
    A class to represent the blog node
    """

    def __init__(self, llm):
        self.llm = llm

    def title_creation(self, state:BlogState):
        """
        Create the title of the Blog
        """
        if "topic" in state and state["topic"]:
            prompt ="""
                    You are an expert blog content writer. Use markdown formatting. Generate a blog title for the topic {topic} strictly within 30 words. This title should be creative and SEO friendly.
                    """
            system_message = prompt.format(topic = state["topic"])
            response = self.llm.invoke(system_message)
            title = extract_text(response.content)
            return {"blog": {"title": title}}
        
    def content_generation(self, state:BlogState):
        if "topic" in state and state['topic']:
            system_prompt = """You are an expert blog writer. use markdown formatting. Generate a detailed blog content with detailed breakdown for the topic {topic}
            """
            system_message = system_prompt.format(topic = state["topic"])
            response = self.llm.invoke(system_message)
            content = extract_text(response.content)
            return {"blog": {"title": state['blog']['title'], "content": content}}
        
    def fetch_images(self, state: BlogState):
        prompt = f"Give 2-3 short image search keywords (comma separated, no explanation) for a blog about: {state['topic']}"
        response = self.llm.invoke(prompt)
        keywords = extract_text(response.content).strip()

        images = []
        for keyword in keywords.split(",")[:3]:
            res = requests.get(
                "https://api.unsplash.com/search/photos",
                params={"query": keyword.strip(), "per_page": 1},
                headers={"Authorization": f"Client-ID {os.getenv('UNSPLASH_ACCESS_KEY')}"}
            )
            data = res.json()
            if data.get("results"):
                img = data["results"][0]
                images.append({
                    "url": img["urls"]["regular"],
                    "alt": img["alt_description"] or keyword.strip(),
                    "credit": img["user"]["name"]
                })

        return {"images": images}
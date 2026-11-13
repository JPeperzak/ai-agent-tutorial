import requests

from agent.data_processing.chunker import TextChunker
from agent.data_processing.embedder import Embedder
from agent.data_processing.temp_index import TemporaryIndex

from agent.models.data_types import ToolResult

API_URL = "https://en.wikipedia.org/w/api.php"
HEADERS = {"User-Agent": "AIAgentTutorial/0.1 (personal learning project)"}
MAX_CHARS = 40_000

class SearchWikipediaTool:
    def __init__(
            self, 
            embedder: Embedder, 
            chunker: TextChunker
    ):
        self.embedder = embedder
        self.chunker = chunker

    def __call__(
            self,
            topic: str,
            query: str,
            top_k: int = 5
    ) -> ToolResult:
        title = self._find_title(topic)
        if title is None:
            return ToolResult(message=f"No Wikipedia article found for '{topic}'.")

        text = self._fetch_article_text(title)
        if not text:
            return ToolResult(message=f"The Wikipedia article '{title}' has no text content.")

        index = TemporaryIndex(self.embedder, self.chunker)
        index.add_text(f"Wikipedia: {title}", text[:MAX_CHARS])
        passages = index.search(query, top_k)
        if not passages:
            return ToolResult(message=f"The Wikipedia article '{title}' has nothing relevant to '{query}'.")
        return ToolResult(passages=passages)


    def _find_title(self, topic: str) -> str | None:
        params = {
            "action": "query",
            "list": "search",
            "srsearch": topic,
            "srlimit": 1,
            "format": "json",
        }
        response = requests.get(API_URL, params=params, headers=HEADERS, timeout=10)
        response.raise_for_status()
        results = response.json()["query"]["search"]
        return results[0]["title"] if results else None

    def _fetch_article_text(self, title: str) -> str:
        params = {
            "action": "query",
            "prop": "extracts",
            "explaintext": 1,
            "titles": title,
            "redirects": 1,
            "format": "json",
        }
        response = requests.get(API_URL, params=params, headers=HEADERS, timeout=10)
        response.raise_for_status()
        page = next(iter(response.json()["query"]["pages"].values()))
        return page.get("extract", "")
import requests
import trafilatura

# DDGS allows you to use web search services. You can use .text to run a regular web search.
from ddgs import DDGS
from ddgs.exceptions import DDGSException

from agent.data_processing.chunker import TextChunker
from agent.data_processing.embedder import Embedder
from agent.data_processing.temp_index import TemporaryIndex

from agent.models.data_types import ToolResult

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; AIAgentTutorial/0.1)"}
MAX_CHARS = 30_000  # per page

class SearchWebTool:
    def __init__(
            self,
            embedder: Embedder,
            chunker: TextChunker,
            max_pages: int = 3
    ):
        self.embedder = embedder
        self.chunker = chunker
        self.max_pages = max_pages

    def __call__(
            self,
            query: str,
            top_k: int = 5
    ) -> ToolResult:
        try:
            # Note that max_results is set higher than the max_pages because some pages might end up unreadable
            # A hit has the format: {"title": title, "href": url, "body": content}
            hits = DDGS().text(query, max_results=self.max_pages + 3)
        except DDGSException as e:
            return ToolResult(message=f"Web search failed: {e}")
        if not hits:
            return ToolResult(message=f"No web results found for '{query}'.")

        index = TemporaryIndex(self.embedder, self.chunker)
        pages_loaded = 0
        # Basically, we go over all the pages we found, chunk/embed them if readable, and store the embeddings in the temporary storage
        for hit in hits:
            if pages_loaded >= self.max_pages:
                break
            text = self._fetch_page_text(hit["href"])
            if text:
                index.add_text(hit["href"], text[:MAX_CHARS])
                pages_loaded += 1

        if pages_loaded == 0:
            return ToolResult(message="Web results were found, but none of the pages could be read.")
        # After the temporary storage is filled with embeddings, we run the embedded query against the embedded chunks to find the k most similar chunks.
        passages = index.search(query, top_k)
        if not passages:
            return ToolResult(message=f"The fetched web pages have nothing relevant to '{query}'.")
        return ToolResult(passages=passages)
        

    def _fetch_page_text(self, url: str) -> str | None:
        try:
            response = requests.get(url, headers=HEADERS, timeout=10)
            response.raise_for_status()
        except requests.RequestException:
            return None
        # Skip PDFs, images, etc. 
        if "text/html" not in response.headers.get("Content-Type", ""):
            return None
        # This returns either a string with content or None if no main text could be found.
        return trafilatura.extract(response.text)
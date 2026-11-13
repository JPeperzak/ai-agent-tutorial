from agent.models.data_processing import (
    DocumentChunkModel
)

from typing import List

class TextChunker:
    def chunk_document(
            self,
            filename: str,
            text: str,
            chunk_size: int = 500,         # Amount of characters per chunk
            overlap: int = 100
    ) -> List[DocumentChunkModel]:
        
        chunks = []
        start = 0
        chunk_index = 0
        # While there is still unchunked content in the document, define and append new chunks
        while start < len(text):
            end = start + chunk_size
            content = text[start:end]
            chunks.append(DocumentChunkModel(
                filename=filename,
                chunk_index=chunk_index,
                content=content
            ))
            chunk_index += 1
            start += chunk_size - overlap
        return chunks
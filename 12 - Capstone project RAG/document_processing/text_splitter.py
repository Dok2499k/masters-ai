from typing import List, Any
from langchain.text_splitters import RecursiveCharacterTextSplitter

class DocumentTextSplitter:

    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200) -> None:
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap
        )

    def split_documents(self, documents: List[Any]) -> List[str]:
        return self.text_splitter.split_documents(documents)
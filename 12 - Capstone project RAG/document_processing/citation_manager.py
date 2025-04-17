from typing import List, Tuple, Optional


class CitationManager:
    def __init__(self) -> None:
        # Stores citations as dictionaries; each may include a document name, page number, and optional chunk index.
        self.citations = []

    def add_citation(self, document_name: str, page_number: int, chunk_index: Optional[int] = None) -> None:
        citation = {
            "document": document_name,
            "page": page_number,
            "chunk": chunk_index
        }
        self.citations.append(citation)

    def get_citations(self) -> List[Tuple[str, int, Optional[int]]]:
        return [(citation["document"], citation["page"], citation.get("chunk")) for citation in self.citations]

    def clear_citations(self) -> None:
        self.citations = []

    def format_citation(self, citation: Tuple[str, int, Optional[int]], show_chunk: bool = False) -> str:
        document, page, chunk = citation
        if show_chunk and chunk is not None:
            return f"{document} (Page {page}, Chunk {chunk})"
        else:
            return f"{document} (Page {page})"

    def format_all_citations(self, show_chunk: bool = False) -> List[str]:
        return [self.format_citation(citation, show_chunk) for citation in self.get_citations()]

    def attach_citation(self, text_chunk: str, document_name: str, page_number: int,
                        chunk_index: Optional[int] = None) -> str:
        self.add_citation(document_name, page_number, chunk_index)
        citation_str = self.format_citation((document_name, page_number, chunk_index))
        return f"{text_chunk}\n\n{citation_str}"

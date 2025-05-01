from typing import List, Dict, Tuple
import re
from pathlib import Path

class TextChunker:
    def __init__(self, chunk_size: int = 1000, overlap: int = 100):
        self.chunk_size = chunk_size
        self.overlap = overlap
        self.chunks: List[str] = []
        self.chunk_summaries: Dict[int, str] = {}
        
    def load_text(self, file_path: str) -> None:
        """Load text from file and split into chunks."""
        text = Path(file_path).read_text(encoding='utf-8')
        
        # Split on paragraphs (double newlines)
        paragraphs = re.split(r'\n\n+', text)
        
        current_chunk = []
        current_length = 0
        
        for para in paragraphs:
            para = para.strip()
            if not para:
                continue
                
            # If adding this paragraph would exceed chunk size, save current chunk
            if current_length + len(para) > self.chunk_size and current_chunk:
                self.chunks.append('\n\n'.join(current_chunk))
                # Keep last paragraph for overlap if needed
                if self.overlap > 0 and current_chunk:
                    current_chunk = [current_chunk[-1]]
                    current_length = len(current_chunk[-1])
                else:
                    current_chunk = []
                    current_length = 0
                    
            current_chunk.append(para)
            current_length += len(para)
        
        # Add final chunk if anything remains
        if current_chunk:
            self.chunks.append('\n\n'.join(current_chunk))
            
        # Generate summaries for each chunk
        self._generate_summaries()
    
    def _generate_summaries(self) -> None:
        """Generate a brief summary for each chunk based on first sentence or character limit."""
        for i, chunk in enumerate(self.chunks):
            # Get first sentence or first 100 chars if no sentence end found
            summary = chunk.split('.')[0][:100] + '...'
            self.chunk_summaries[i] = summary
            
    def get_chunk(self, index: int) -> str:
        """Get a specific chunk by index."""
        if 0 <= index < len(self.chunks):
            return self.chunks[index]
        raise IndexError("Chunk index out of range")
    
    def get_relevant_chunks(self, query: str, num_chunks: int = 3) -> List[Tuple[int, str]]:
        """
        Get most relevant chunks for a query based on simple keyword matching.
        Returns list of (chunk_index, chunk_text) tuples.
        """
        # Simple relevance scoring based on keyword matches
        scores = []
        query_words = set(query.lower().split())
        
        for i, chunk in enumerate(self.chunks):
            chunk_words = set(chunk.lower().split())
            score = len(query_words.intersection(chunk_words))
            scores.append((score, i))
            
        # Sort by score descending and return top chunks
        scores.sort(reverse=True)
        relevant_chunks = []
        for _, chunk_idx in scores[:num_chunks]:
            relevant_chunks.append((chunk_idx, self.chunks[chunk_idx]))
            
        return relevant_chunks

def get_context_for_query(query: str, lore_file: str = "data/lore.txt", num_chunks: int = 2) -> str:
    """
    Helper function to get relevant context for a specific query.
    Returns concatenated relevant chunks.
    """
    chunker = TextChunker()
    chunker.load_text(lore_file)
    relevant_chunks = chunker.get_relevant_chunks(query, num_chunks)
    return "\n\n---\n\n".join(chunk for _, chunk in relevant_chunks) 
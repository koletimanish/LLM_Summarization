import re
import requests

from typing import Tuple, List
from bs4 import BeautifulSoup
from app.core.config import settings

class DataProcessor:
    @staticmethod
    def clean_text(text: str) -> str:
        text = re.sub(r'\s+', ' ', text) # Remove extra whitespace
        text = re.sub(r'[^\w\s.,!?-]', '', text) # Remove special characters but keep basic punctuation
        return text.strip()

    @staticmethod
    def process_input(data: str) -> Tuple[str, str]:
        return DataProcessor.clean_text(data)

    # Unnecessary for now, but could be useful for future reference/implementations
    @staticmethod
    def chunk_text(text: str, max_length: int = settings.MAX_INPUT_LENGTH) -> List[str]:
        # Current max is 8000 tokens
        words = text.split()
        chunks = []
        current_chunk = []
        current_length = 0

        for word in words:
            if current_length + len(word) + 1 > max_length:
                chunks.append(' '.join(current_chunk))
                current_chunk = [word]
                current_length = len(word)
            else:
                current_chunk.append(word)
                current_length += len(word) + 1

        if current_chunk:
            chunks.append(' '.join(current_chunk))

        return chunks 
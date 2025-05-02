import re
from typing import Tuple, List
import requests
from bs4 import BeautifulSoup
from app.core.config import settings

class DataProcessor:
    @staticmethod
    def clean_text(text: str) -> str:
        """Clean and normalize input text."""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s.,!?-]', '', text)
        return text.strip()

    @staticmethod
    def extract_from_url(url: str) -> Tuple[str, str]:
        """Extract text content from a URL."""
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Get text content
            text = soup.get_text()
            source = url
            
            return DataProcessor.clean_text(text), source
        except Exception as e:
            raise ValueError(f"Failed to extract content from URL: {str(e)}")

    @staticmethod
    def process_input(data: str) -> Tuple[str, str]:
        """Process input data, handling both direct text and URLs."""
        if data.startswith(('http://', 'https://')):
            return DataProcessor.extract_from_url(data)
        return DataProcessor.clean_text(data), "direct_input"

    @staticmethod
    def chunk_text(text: str, max_length: int = settings.MAX_INPUT_LENGTH) -> List[str]:
        """Split text into chunks of maximum length."""
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
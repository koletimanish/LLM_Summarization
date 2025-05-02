from typing import List, Dict, Any
import time
from openai import OpenAI
from app.core.config import settings
from app.models.schemas import Citation

class LLMService:
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.DEFAULT_MODEL
    
    def _test_model(self):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": "Hello, how are you?"}]
        )
        return response.choices[0].message.content
    
    def _generate_messy_data(self, row_data):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": "Generate messy startup data"}]
        )
        return response.choices[0].message.content

    def _create_system_prompt(self) -> str:
        return """You are an expert startup data analyst. Your task is to analyze and summarize startup-related information.
        Provide a clear, concise summary with specific citations from the source material.
        Focus on key metrics, funding information, market position, and growth potential.
        Format your response as a JSON object with the following structure:
        {
            "summary": "Your concise summary here",
            "citations": [
                {
                    "text": "The exact quote or fact",
                    "source": "Where this information came from"
                }
            ]
        }"""

    def _create_user_prompt(self, text: str, max_length: int) -> str:
        return f"""Please analyze the following startup data and provide a summary of maximum {max_length} words:

{text}

Remember to include specific citations and maintain a professional tone."""

    async def generate_summary(self, text: str, max_length: int = 500) -> Dict[str, Any]:
        start_time = time.time()
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self._create_system_prompt()},
                    {"role": "user", "content": self._create_user_prompt(text, max_length)}
                ],
                temperature=settings.TEMPERATURE,
                max_tokens=settings.MAX_TOKENS
            )
            
            # Extract the response content
            content = response.choices[0].message.content
            
            # Parse the JSON response
            import json
            result = json.loads(content)
            
            # Add processing metadata
            processing_time = time.time() - start_time
            
            return {
                "summary": result["summary"],
                "citations": [
                    Citation(
                        text=citation["text"],
                        source=citation["source"],
                        timestamp=None
                    ) for citation in result["citations"]
                ],
                "metadata": {
                    "processing_time": processing_time,
                    "model_used": self.model
                }
            }
            
        except Exception as e:
            raise Exception(f"Error generating summary: {str(e)}")

    async def process_large_text(self, text: str, max_length: int = 500) -> Dict[str, Any]:
        """Process large texts by chunking and combining summaries."""
        from app.services.data_processor import DataProcessor
        
        chunks = DataProcessor.chunk_text(text)
        summaries = []
        all_citations = []
        
        for chunk in chunks:
            result = await self.generate_summary(chunk, max_length // len(chunks))
            summaries.append(result["summary"])
            all_citations.extend(result["citations"])
        
        # Combine summaries
        combined_summary = " ".join(summaries)
        
        # Generate final summary of combined summaries
        final_result = await self.generate_summary(combined_summary, max_length)
        
        return final_result 
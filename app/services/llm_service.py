import time
import json
from datetime import datetime

from typing import List, Dict, Any
from openai import OpenAI
from app.core.config import settings

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
        row_data = row_data.to_dict()
        structured_json = json.dumps(row_data, indent=2)

        print(structured_json)

        prompt = f"""You are a tech or business journalist writing a short paragraph based on structured startup data. 
            Each paragraph should sound natural, as if it were taken from an article, press release, blog post, or investor newsletter.

            Here are your writing rules:
            - First, check if there is funding data (funding_round_type, funding_round_code, raised_amount). If present, write a funding-focused summary.
            - Only if there is no funding data, write about acquisition data (if available).
            - Vary the tone: some summaries can be formal, others casual or speculative.
            - Vary the focus: some may emphasize funding, others the product, the location, the acquisition, or the industry.
            - Do NOT try to include all the fields. Select a few that feel relevant and omit the rest.
            - You MUST always mention:
                - For funding summaries: the company name, funding round details, amount raised, and the source (funding_source_url)
                - For acquisition summaries: the company name, acquiring company, price, and the source (acquisition_source_url)
            - Avoid bullet points or lists. Return only a natural paragraph that is not too long.

            Structured data:
            {structured_json}
        """

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7  # Add temperature for variation
        )
        return response.choices[0].message.content

    def _create_system_prompt(self) -> str:
        return """You are an intelligent information extractor that analyzes messy or unstructured descriptions of startups.

        Given a paragraph describing a startup, extract the relevant information and return it in a structured JSON format using the following fields:

        - name: string (required, acquired/funded company name)
        - industry: string (optional, if available)
        - location: string (optional, if available)
        - founded_year: string (optional, if available)
        - funding_total_usd: string (optional, if available)
        - funding_stage: string (e.g. Seed, Series A, Series B, etc. — optional, if available)
        - investors: list of strings (optional, if available)
        - acquiring_company: string (optional, if available)
        - acquisition_date: string in YYYY-MM-DD format (optional, if available)
        - acquisition_price: string (optional, if available)
        - source: string (must be included will typically be a URL, put "From Kaggle" if not available)

        If a field is not mentioned in the input, omit it entirely from the JSON. Do not guess or make up information.

        Always return a valid JSON object — no comments, extra text, or explanations.

        Examples of valid output:
        {
        "name": "Fintrack",
        "industry": "Fintech",
        "location": "New York",
        "founded_year": 2020,
        "funding_stage": "Series A",
        "investors": ["Sequoia Capital"],
        "acquiring_company": "Plaid",
        "acquisition_date": "2021-01-01",
        "acquisition_price": "100M",
        "source": "www.techcrunch.com"
        }"""

    def _create_user_prompt(self, text: str, max_length: int) -> str:
        return f"""Please analyze the following startup data and provide a summary of maximum {max_length} words:

        {text}

        Remember to include specific citations from the provided text and maintain a professional tone."""

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
            startup_info = json.loads(content)
            
            # Add processing metadata
            processing_time = time.time() - start_time
            
            return {
                "startup_info": startup_info,
                "metadata": {
                    "processing_time": processing_time,
                    "model_used": self.model,
                    "timestamp": datetime.utcnow()
                }
            }
            
        except Exception as e:
            raise Exception(f"Error generating summary: {str(e)}") 
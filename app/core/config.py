import os

from pydantic_settings import BaseSettings
from functools import lru_cache
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Startup Data Summarizer"
    
    # OpenAI Settings
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    
    # Model Settings
    DEFAULT_MODEL: str = "gpt-4o-mini"
    MAX_TOKENS: int = 2000
    TEMPERATURE: float = 0.7
    
    # Data Processing Settings
    MAX_INPUT_LENGTH: int = 8000
    MIN_SUMMARY_LENGTH: int = 100
    MAX_SUMMARY_LENGTH: int = 500

settings = Settings()
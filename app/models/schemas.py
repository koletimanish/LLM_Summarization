from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

# User request schema
class SummarizeRequest(BaseModel):
    data: str = Field(..., description="Raw startup data text")
    max_length: Optional[int] = Field(500, description="Maximum length of the summary in words")

# LLM response schema
class LLMSummarizationResponse(BaseModel):
    name: str
    industry: Optional[str] = None
    location: Optional[str] = None
    founded_year: Optional[int] = None
    funding_total_usd: Optional[str] = None
    funding_stage: Optional[str] = None
    investors: Optional[List[str]] = None
    acquiring_company: Optional[str] = None
    acquisition_date: Optional[str] = None
    acquisition_price: Optional[str] = None
    source: str

# Unnecessary for now, but could be useful for future reference/implementations
class Metadata(BaseModel):
    processing_time: float
    model_used: str
    timestamp: datetime

# API response schema
class SummarizeResponse(BaseModel):
    startup_info: LLMSummarizationResponse
    metadata: Metadata

# Error response schema
class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None 
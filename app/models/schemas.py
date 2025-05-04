from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class SummarizeRequest(BaseModel):
    data: str = Field(..., description="Raw startup data text or URL to process")
    max_length: Optional[int] = Field(500, description="Maximum length of the summary in words")
    model: Optional[str] = Field("gpt-4o-mini", description="LLM model to use for summarization")

class StartupInfo(BaseModel):
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

class Metadata(BaseModel):
    processing_time: float
    model_used: str
    timestamp: datetime

class SummarizeResponse(BaseModel):
    startup_info: StartupInfo
    metadata: Metadata

class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None 
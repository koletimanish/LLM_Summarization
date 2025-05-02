from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class SummarizeRequest(BaseModel):
    data: str = Field(..., description="Raw startup data text or URL to process")
    max_length: Optional[int] = Field(500, description="Maximum length of the summary in words")
    model: Optional[str] = Field("gpt-4", description="LLM model to use for summarization")

class Citation(BaseModel):
    text: str
    source: str
    timestamp: Optional[datetime]

class Metadata(BaseModel):
    source: str
    timestamp: datetime
    processing_time: float
    model_used: str

class SummarizeResponse(BaseModel):
    summary: str
    citations: List[Citation]
    metadata: Metadata

class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None 
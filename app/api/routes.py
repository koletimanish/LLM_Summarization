from fastapi import APIRouter, HTTPException
from app.models.schemas import SummarizeRequest, SummarizeResponse, ErrorResponse
from app.services.data_processor import DataProcessor
from app.services.llm_service import LLMService
from datetime import datetime

router = APIRouter()
llm_service = LLMService()

@router.post(
    "/summarize",
    response_model=SummarizeResponse,
    responses={
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    }
)

async def summarize_data(request: SummarizeRequest):
    try:
        # Process input data
        processed_text = DataProcessor.process_input(request.data)

        print(processed_text)
        
        # Generate summary directly
        result = await llm_service.generate_summary(
            processed_text,
            max_length=request.max_length
        )

        print(result)
        
        return SummarizeResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while processing your request: {str(e)}"
        ) 
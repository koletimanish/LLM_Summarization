from fastapi import APIRouter, HTTPException
from app.models.schemas import SummarizeRequest, SummarizeResponse, ErrorResponse
from app.services.data_processor import DataProcessor
from app.services.llm_service import LLMService
from datetime import datetime

router = APIRouter()
llm_service = LLMService()

# Only route for now, can add more routes later depending on expanding the scenario
@router.post(
    "/summarize",
    response_model=SummarizeResponse,
    responses={
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    }
)

# async specifically so we can use async LLM service with requests
async def summarize_data(request: SummarizeRequest):
    try:
        processed_text = DataProcessor.process_input(request.data)

        print(processed_text)
        
        # Generate summary directly with no pre-processing
        # Assumes the input text is not too long and the LLM can handle it
        result = await llm_service.generate_summary(
            processed_text,
            max_length=request.max_length
        )
        
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
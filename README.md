# LLM Startup Data Summarization Microservice

This microservice processes raw startup data and generates structured summaries using LLM technology. It can handle both funding and acquisition data, providing natural language summaries with proper citations.

## Features

- Data ingestion and cleaning
- LLM-powered summarization with funding/acquisition focus
- Structured JSON output with citations
- RESTful API interface
- Docker support

## Project Structure

```
.
├── app/
│   ├── api/
│   │   └── routes.py          # FastAPI routes and endpoints
│   ├── core/
│   │   └── config.py         # Application settings and configuration
│   ├── services/
│   │   ├── data_processor.py # Text processing and cleaning
│   │   └── llm_service.py    # LLM integration and prompt management
│   └── models/
│       └── schemas.py        # Pydantic models for request/response
├── data/
│   ├── raw/                  # Raw data files
|   |   |--...
│   └── processed/            # Processed data output
|   |   |--...
├── notebooks/                # Jupyter notebooks for analysis
|   |   |--- messy_data_gen.ipynb
├── Dockerfile
├── requirements.txt          # All python library dependencies
└── main.py                   # Application entry point
└── README.md                   # Project overview
```

## Setup Instructions
### I created this project on an M1 Macbook Pro, so adjust any of these commands as necessary

1. Create a virtual environment:
```bash
python -m venv env
source env/bin/activate
```

2. Install dependencies:
```bash
pip3 install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file in the root directory with:
```
OPENAI_API_KEY=your_api_key_here
```

4. Run the application:
```bash
uvicorn main:app --reload
```

## API Usage

### Summarizing Startup Data

**Endpoint:** `POST /api/v1/summarize`

**Request Body:**
```json
{
    "data": "Raw startup data text here",
    "max_length": 500
}
```

**Response:**
```json
{
    "startup_info": {
        "name": "Company Name",
        "industry": "Industry",
        "location": "Location",
        "founded_year": "Year",
        "funding_total_usd": "Amount",
        "funding_stage": "Stage",
        "investors": ["Investor 1", "Investor 2"],
        "acquiring_company": "Acquirer Name",
        "acquisition_date": "Date",
        "acquisition_price": "Amount",
        "source": "Source"
    },
    "metadata": {
        "processing_time": 1.23,
        "model_used": "gpt-4o-mini",
        "timestamp": "2024-01-01T12:00:00Z"
    }
}
```

## Features in Detail

### Data Processing
- Text cleaning and normalization
- Support for both funding and acquisition data
- Automatic detection of inputted summary type needed (funding vs acquisition)

### LLM Integration
- Structured prompt engineering
- Temperature for varied outputs

### API Features
- Async request handling
- Input validation
- Structured error responses
- CORS support

## Docker Support

Build and run with Docker:
```bash
docker build -t startup-summarizer .
docker run -p 8000:8000 startup-summarizer
```

## License

MIT 
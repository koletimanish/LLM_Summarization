# LLM Startup Data Summarization Microservice

This microservice processes raw startup data and generates structured summaries with citations using LLM technology.

## Features

- Data ingestion and cleaning
- LLM-powered summarization
- Structured output with citations
- RESTful API interface
- Docker support

## Project Structure

```
.
├── app/
│   ├── api/
│   │   └── routes.py
│   ├── core/
│   │   ├── config.py
│   │   └── security.py
│   ├── services/
│   │   ├── data_processor.py
│   │   └── llm_service.py
│   └── models/
│       └── schemas.py
├── data/
│   └── raw/
├── notebooks/
│   └── analysis.ipynb
├── tests/
├── Dockerfile
├── requirements.txt
└── main.py
```

## Setup Instructions

1. Create a virtual environment:
```bash
python -m venv env
source env/bin/activate  # On Windows: .\env\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
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

### Summarize Startup Data

**Endpoint:** `POST /api/v1/summarize`

**Request Body:**
```json
{
    "data": "Raw startup data text or URL",
    "max_length": 500
}
```

**Response:**
```json
{
    "summary": "Structured summary of the startup data",
    "citations": ["citation1", "citation2"],
    "metadata": {
        "source": "data_source",
        "timestamp": "2023-11-15T12:00:00Z"
    }
}
```

## Docker Support

Build and run with Docker:
```bash
docker build -t startup-summarizer .
docker run -p 8000:8000 startup-summarizer
```

## Data Sources

The service is designed to work with various startup datasets, including:
- Crunchbase data
- Startup news articles
- Company reports
- Market analysis documents

## License

MIT 
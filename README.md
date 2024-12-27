# SLIK Report Analyzer

A tool to analyze Indonesian SLIK (Sistem Layanan Informasi Keuangan) reports using OCR and LLM technologies. This project includes both a Streamlit web interface and a REST API.

## Prerequisites

- Python 3.8 or higher
- Docker
- OpenAI API key

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/slik-analyzer.git
cd slik-analyzer
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env file and add your OpenAI API key
```

## Setting up LLMSherpa

LLMSherpa is used for PDF processing and OCR. Follow these steps to set it up:

1. Pull the Docker image:
```bash
docker pull ghcr.io/nlmatics/nlm-ingestor:latest
```

2. Run the Docker container:
```bash
docker run -p 5010:5001 ghcr.io/nlmatics/nlm-ingestor:latest
```

This will start the LLMSherpa server at `http://localhost:5010`.

## Running the Applications

### Starting the API Server

The API provides endpoints for processing and analyzing SLIK reports:

```bash
uvicorn src.api:app --reload --port 8000
```

API endpoints will be available at:
- API documentation: http://localhost:8000/docs
- Main endpoints:
  - POST `/process-slik`: Process a SLIK PDF file
  - POST `/analyze-slik`: Process and analyze a SLIK PDF file
  - POST `/analyze-json`: Analyze already processed SLIK data

### Running the Streamlit Interface

The Streamlit interface provides a user-friendly way to interact with the system:

```bash
streamlit run src/streamlit_app.py
```

The web interface will be available at http://localhost:8501

## Project Structure

```
ideb-slik-parser/
├── .env
├── requirements.txt
├── src/
│   ├── __init__.py
│   ├── models.py      # Pydantic models
│   ├── processor.py   # SLIK processing logic
│   ├── analyzer.py    # Analysis logic
│   ├── api.py        # FastAPI implementation
│   └── streamlit_app.py  # Streamlit interface
```


## Environment Variables

Create a `.env` file with the following variables:

```env
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# LLMSherpa Configuration
LLMSHERPA_API_URL=http://localhost:5010/api/parseDocument?renderFormat=all

# Alibaba Cloud Model Studio Configuration
MODEL_STUDIO_API_KEY=your_model_studio_api_key_here
MODEL_STUDIO_BASE_URL=https://your-model-studio-endpoint.url
```

### Environment Variable Details

- `OPENAI_API_KEY`: Your OpenAI API key for GPT models
- `LLMSHERPA_API_URL`: URL for the LLMSherpa PDF processor
- `MODEL_STUDIO_API_KEY`: Your Alibaba Cloud Model Studio API key for accessing Qwen models
- `MODEL_STUDIO_BASE_URL`: Base URL for your Model Studio endpoint (specific to your Alibaba Cloud region and deployment)

### Example .env.example file:
```env
OPENAI_API_KEY=sk-...
LLMSHERPA_API_URL=http://localhost:5010/api/parseDocument?renderFormat=all
MODEL_STUDIO_API_KEY=ak-...
MODEL_STUDIO_BASE_URL=https://dashscope-intl.aliyuncs.com/compatible-mode/v1
```

## API Usage Examples

1. Process a SLIK PDF file:
```bash
curl -X POST "http://localhost:8000/process-slik" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@your_slik.pdf"
```

2. Process and analyze a SLIK PDF file:
```bash
curl -X POST "http://localhost:8000/analyze-slik" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@your_slik.pdf"
```

3. Analyze processed SLIK data:
```bash
curl -X POST "http://localhost:8000/analyze-json" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{"slik_data": {...}}'
```

## Troubleshooting

1. If port 8000 is already in use:
```bash
# Find the process using the port
sudo lsof -i :8000
# Kill the process
sudo kill <PID>
# Or use a different port
uvicorn src.api:app --reload --port 8001
```

2. If LLMSherpa server is not responding:
- Ensure Docker is running
- Check if the container is running: `docker ps`
- Check container logs: `docker logs <container_id>`

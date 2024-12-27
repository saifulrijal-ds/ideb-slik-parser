# src/api.py
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from typing import Dict, Any
from .processor import SLIKProcessor
from .analyzer import SLIKAnalyzer
from .models import SLIKReport
import json
from pydantic import BaseModel

app = FastAPI(title="SLIK Processor API")

# Initialize processors
processor = SLIKProcessor()
analyzer = SLIKAnalyzer()

class AnalyzeRequest(BaseModel):
    """Request model for analysis endpoint when sending processed SLIK data"""
    slik_data: Dict[str, Any]

@app.post("/process-slik")
async def process_slik(file: UploadFile = File(...)):
    """Process a SLIK PDF file and return structured data"""
    try:
        content = await file.read()
        result = processor.process_uploaded_file(content)
        return JSONResponse(content=result.model_dump())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze-slik")
async def analyze_slik(file: UploadFile = File(...)):
    """Process a SLIK PDF file and return both structured data and analysis"""
    try:
        # Process the file
        content = await file.read()
        processed_result = processor.process_uploaded_file(content)
        
        # Analyze the processed data
        analysis_result = analyzer.analyze(processed_result)
        
        # Return both processing and analysis results
        return JSONResponse(content={
            "slik_data": processed_result.model_dump(),
            "analysis": analysis_result.model_dump()
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze-json")
async def analyze_json(request: AnalyzeRequest):
    """Analyze already processed SLIK data"""
    try:
        # Convert JSON data to SLIKReport
        slik_report = SLIKReport.model_validate(request.slik_data)
        
        # Analyze the data
        analysis_result = analyzer.analyze(slik_report)
        
        return JSONResponse(content=analysis_result.model_dump())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# If you want to add API documentation
@app.get("/")
async def root():
    return {
        "message": "SLIK Processor API",
        "endpoints": {
            "/process-slik": "Process SLIK PDF and return structured data",
            "/analyze-slik": "Process SLIK PDF and return both data and analysis",
            "/analyze-json": "Analyze already processed SLIK data"
        }
    }
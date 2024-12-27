import os
from pathlib import Path
import tempfile
from langchain_community.document_loaders.llmsherpa import LLMSherpaFileLoader
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from .models import SLIKReport

class SLIKProcessor:
    def __init__(self):
        self.llmsherpa_api_url = os.getenv("LLMSHERPA_API_URL")
        # self.llm = ChatOpenAI(
        #     api_key=os.getenv("OPENAI_API_KEY"),
        #     model="gpt-4o-mini",
        #     temperature=0.1,
        # )

        self.llm = ChatOpenAI(
            api_key=os.getenv("MODEL_STUDIO_API_KEY"),
            model="qwen-turbo",
            base_url=os.getenv("MODEL_STUDIO_BASE_URL"),
            temperature=0.0,
        )
        
        self.prompt = ChatPromptTemplate.from_messages([
            (
                "system",
                """You are an expert financial data extraction algorithm specialized in Indonesian SLIK reports.
                Extract all relevant information from the SLIK report text into structured data.
                Follow these guidelines:
                - Convert all monetary values to numbers (remove 'Rp' and ',' separators)
                - Convert percentage values to decimal numbers
                - Format dates as YYYY-MM-DD
                - If a value is not present in the text, return null
                - Maintain relationships between facilities, collateral, and guarantors
                Be precise and accurate in extracting financial data."""
            ),
            ("human", "{text}")
        ])
        
        self.structured_llm = self.llm.with_structured_output(schema=SLIKReport)
        self.extractor = self.prompt | self.structured_llm

    def process_file(self, file_path: str) -> SLIKReport:
        """Process a SLIK PDF file and return structured data"""
        loader = LLMSherpaFileLoader(
            file_path=file_path,
            new_indent_parser=True,
            apply_ocr=True,
            strategy="text",
            llmsherpa_api_url=self.llmsherpa_api_url,
        )
        docs = loader.load()
        slik_text = docs[0].page_content
        return self.extractor.invoke({"text": slik_text})

    def process_uploaded_file(self, file_content: bytes) -> SLIKReport:
        """Process an uploaded file's content and return structured data"""
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            tmp_file.write(file_content)
            tmp_path = tmp_file.name
            
        try:
            result = self.process_file(tmp_path)
        finally:
            Path(tmp_path).unlink()
            
        return result

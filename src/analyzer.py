from typing import Dict, List
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from .models import SLIKReport
import os

class CreditAnalysis(BaseModel):
    """Structured analysis of SLIK report"""
    credit_score: int = Field(..., description="Credit score from 300-850 based on payment history and credit profile")
    risk_level: str = Field(..., description="Overall risk assessment (Low/Medium/High)")
    key_strengths: List[Dict[str, str]] = Field(..., description="Key positive factors in the credit profile")
    key_concerns: List[Dict[str, str]] = Field(..., description="Key risk factors or concerns")
    payment_behavior: Dict[str, str] = Field(..., description="Analysis of payment patterns and behavior")
    credit_utilization: Dict[str, str] = Field(..., description="Analysis of credit limit usage")
    recommendations: List[Dict[str, str]] = Field(..., description="Actionable recommendations")
    summary: str = Field(..., description="Overall analysis summary")

class SLIKAnalyzer:
    def __init__(self):
        # self.llm = ChatOpenAI(
        #     model="gpt-4",
        #     temperature=0.1,
        # )

        self.llm = ChatOpenAI(
            api_key=os.getenv("MODEL_STUDIO_API_KEY"),
            model="qwen-turbo",
            base_url=os.getenv("MODEL_STUDIO_BASE_URL"),
            temperature=0.0,
        )
        
        self.analysis_prompt = ChatPromptTemplate.from_messages([
            (
                "system",
                """
You are an expert credit analyst specialized in Indonesian banking and credit reporting systems. You have access to parsed SLIK (Sistem Layanan Informasi Keuangan) iDeb report data. Your task is to:

1. Thoroughly analyze the provided SLIK iDeb data.
2. Generate a structured credit analysis following the guidelines below.
3. Present the final results in the specified Python `CreditAnalysis` model format.

**Data Context:**  
- Input: Parsed SLIK iDeb data from an original PDF report. The input includes borrower credit history, outstanding balances, credit limits, payment patterns, credit usage, loan types, and any delinquency records.
- Audience: Credit analysts or other banking/financial institution professionals who use SLIK reports to make informed credit decisions.

**Analysis Guidelines:**

1. **Credit Scoring (300-850):**  
   - Evaluate payment history (e.g., number of days past due, delinquency patterns, recent late payments).  
   - Assess credit utilization (e.g., current usage vs. limits, highest utilization trends).  
   - Consider the length of credit history (e.g., how long accounts have been open, recent account openings).  
   - Factor in the types of credit used (e.g., secured vs. unsecured credit, consumer loans, mortgages).  
   - Combine these factors into a final credit score between 300-850.

2. **Risk Assessment:**  
   - Identify trends in payment behavior (e.g., consistent on-time payments vs. recent delinquencies).  
   - Evaluate credit utilization patterns (e.g., consistently high utilization or recent spikes in usage).  
   - Consider total exposure relative to the borrower’s profile and typical Indonesian banking norms.  
   - Factor in credit mix and the length of credit history for an overall risk classification (Low, Medium, High).

3. **Strengths and Concerns:**  
   - Highlight key strengths such as a long history of timely payments, low utilization, strong credit mix, or recent positive changes.  
   - Flag concerns including high delinquency rates, increasing utilization, numerous recent inquiries, or short account tenure.

4. **Recommendations:**  
   - Provide actionable insights for improving creditworthiness.  
   - Suggest strategies such as reducing utilization, diversifying credit, improving timely payments, or restructuring certain debts.

**Format Guidelines:**
- Be specific, quantitative, and reference data from the provided SLIK iDeb results.  
- Support conclusions with relevant data points (e.g., “Utilization increased from 40% to 75% in the last 6 months”).  
- Offer clear rationale for recommendations.  
- Reflect Indonesian banking norms and consider sector-specific context.  
- Present your final analysis in a Python dictionary conforming to the `CreditAnalysis` schema, e.g.:

```python
{{
  "credit_score": 750,
  "risk_level": "Medium",
  "key_strengths": [
    {{"factor": "Payment History", "detail": "No late payments in the last 12 months"}}
  ],
  "key_concerns": [
    {{"factor": "Credit Utilization", "detail": "Utilization rose from 40% to 75% in the last 6 months"}}
  ],
  "payment_behavior": {{
    "history": "Consistently timely until the last 3 months; one 30-day late payment noted",
    "trend": "Recent dip in timeliness"
  }},
  "credit_utilization": {{
    "current_utilization": "75%",
    "trend": "Significant increase in last 6 months"
  }},
  "recommendations": [
    {{"action": "Reduce Utilization", "suggestion": "Aim to lower utilization below 50%"}},
    {{"action": "Timely Payments", "suggestion": "Ensure all payments are made on or before due date"}}
  ],
  "summary": "Overall, the profile shows historically good payment behavior but a recent uptick in utilization and a late payment raises moderate concerns. Recommended to control utilization and ensure on-time payments to maintain a solid standing."
}}
```

**Additional Considerations:**
- If certain data points are missing, use available information and note any assumptions.  
- Always explain the reasoning behind risk assessments and recommendations.  
- Refer to Indonesian credit quality grades (e.g., Quality 1 = Lancar) and relate these to the analysis where appropriate.
                """
            ),
            ("human", "{report_json}")
        ])
        
        self.structured_llm = self.llm.with_structured_output(schema=CreditAnalysis)
        self.analyzer = self.analysis_prompt | self.structured_llm

    def analyze(self, report: SLIKReport) -> CreditAnalysis:
        """Analyze a SLIK report and return structured insights"""
        report_json = report.model_dump()
        return self.analyzer.invoke({"report_json": report_json})

from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import date

class PaymentHistory(BaseModel):
    """Monthly payment history information."""
    month: Optional[str] = Field(default=None, description="Month of payment record")
    quality: Optional[str] = Field(default=None, description="Credit quality for that month (1-5)")
    days_past_due: Optional[int] = Field(default=None, description="Number of days past due")

class CreditFacility(BaseModel):
    """Information about a credit/financing facility."""
    reporter: Optional[str] = Field(default=None, description="Name of the reporting bank")
    branch: Optional[str] = Field(default=None, description="Branch name")
    agreement_number: Optional[str] = Field(default=None, description="Credit agreement number")
    facility_type: Optional[str] = Field(default=None, description="Type of credit facility")
    plafond: Optional[float] = Field(default=None, description="Credit limit in IDR")
    outstanding: Optional[float] = Field(default=None, description="Current outstanding balance in IDR")
    start_date: Optional[date] = Field(default=None, description="Start date of credit")
    due_date: Optional[date] = Field(default=None, description="Due date of credit")
    interest_rate: Optional[float] = Field(default=None, description="Interest rate percentage")
    interest_type: Optional[str] = Field(default=None, description="Type of interest rate")
    usage_type: Optional[str] = Field(default=None, description="Usage type (e.g., Konsumsi)")
    quality: Optional[str] = Field(default=None, description="Current credit quality")
    days_past_due: Optional[int] = Field(default=None, description="Current days past due")
    payment_history: List[PaymentHistory] = Field(default_factory=list, description="12-month payment history")

class SLIKReport(BaseModel):
    """SLIK report information."""
    report_number: Optional[str] = Field(default=None, description="SLIK report number")
    report_date: Optional[date] = Field(default=None, description="Date of the SLIK report")
    reference_number: Optional[str] = Field(default=None, description="Reference number")
    operator: Optional[str] = Field(default=None, description="Operator name")
    debtor_name: Optional[str] = Field(default=None, description="Name of the debtor")
    debtor_id: Optional[str] = Field(default=None, description="ID number/NIK of the debtor")
    gender: Optional[str] = Field(default=None, description="Gender of debtor")
    birth_place: Optional[str] = Field(default=None, description="Place of birth")
    birth_date: Optional[date] = Field(default=None, description="Date of birth")
    address: Optional[str] = Field(default=None, description="Complete address")
    occupation: Optional[str] = Field(default=None, description="Occupation")
    workplace: Optional[str] = Field(default=None, description="Workplace name")
    total_plafond: Optional[float] = Field(default=None, description="Total effective plafond")
    total_outstanding: Optional[float] = Field(default=None, description="Total outstanding balance")
    worst_quality: Optional[str] = Field(default=None, description="Worst credit quality")
    facilities: List[CreditFacility] = Field(default_factory=list, description="List of credit facilities")

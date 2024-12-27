# src/streamlit_app.py
import streamlit as st
from .processor import SLIKProcessor
from .analyzer import SLIKAnalyzer, CreditAnalysis  # Added analyzer imports
import pandas as pd
import plotly.express as px
import json
import time
from typing import Dict, List  # For type hints

def display_analysis(analysis):
    st.header("Credit Analysis")
    
    # Credit Score and Risk Level
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Credit Score", analysis.credit_score)
    with col2:
        st.metric("Risk Level", analysis.risk_level)
    
    # Summary
    st.subheader("Analysis Summary")
    st.write(analysis.summary)
    
    # Debug: Print the structure
    st.write("Debug - Analysis structure:", analysis.model_dump())
    
    # Strengths and Concerns
    col3, col4 = st.columns(2)
    with col3:
        st.subheader("Key Strengths")
        for strength in analysis.key_strengths:
            # Check if strength is a dictionary and has required keys
            if isinstance(strength, dict) and "title" in strength and "description" in strength:
                with st.expander(strength["title"]):
                    st.write(strength["description"])
            else:
                st.write(strength)  # Just display the strength as is if not in expected format
    
    with col4:
        st.subheader("Key Concerns")
        for concern in analysis.key_concerns:
            # Check if concern is a dictionary and has required keys
            if isinstance(concern, dict) and "title" in concern and "description" in concern:
                with st.expander(concern["title"]):
                    st.write(concern["description"])
            else:
                st.write(concern)  # Just display the concern as is if not in expected format
    
    # Payment Behavior
    st.subheader("Payment Behavior Analysis")
    for key, value in analysis.payment_behavior.items():
        with st.expander(key):
            st.write(value)
    
    # Credit Utilization
    st.subheader("Credit Utilization Analysis")
    for key, value in analysis.credit_utilization.items():
        with st.expander(key):
            st.write(value)
    
    # Recommendations
    st.subheader("Recommendations")
    for rec in analysis.recommendations:
        # Check if recommendation is a dictionary and has required keys
        if isinstance(rec, dict) and "title" in rec and "description" in rec:
            with st.expander(rec["title"]):
                st.write(rec["description"])
        else:
            st.write(rec)  # Just display the recommendation as is if not in expected format

@st.fragment
def fragment_generate_analysis(report):
    if st.button("Generate Credit Analysis"):
        with st.spinner("Analyzing credit profile..."):
            analyzer = SLIKAnalyzer()
            analysis = analyzer.analyze(report)
            display_analysis(analysis)

def display_slik_summary(report, raw_json):
    """Display SLIK report summary in Streamlit"""
    # Basic Information
    st.header("SLIK Report Summary")
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Report Details")
        st.write(f"Report Number: {report.report_number}")
        st.write(f"Report Date: {report.report_date}")
        st.write(f"Reference Number: {report.reference_number}")
        st.write(f"Operator: {report.operator}")
    
    with col2:
        st.subheader("Debtor Information")
        st.write(f"Name: {report.debtor_name}")
        st.write(f"ID: {report.debtor_id}")
        st.write(f"Gender: {report.gender}")
        st.write(f"Birth: {report.birth_place}, {report.birth_date}")

    # Credit Summary
    st.subheader("Credit Summary")
    col3, col4, col5 = st.columns(3)
    
    with col3:
        st.metric("Total Plafond", f"Rp {report.total_plafond:,.2f}")
    with col4:
        st.metric("Outstanding Balance", f"Rp {report.total_outstanding:,.2f}")
    with col5:
        st.metric("Credit Quality", report.worst_quality)

    # Payment History Visualization
    if report.facilities:
        st.subheader("Payment History")
        facility = report.facilities[0]  # Assuming we're showing the first facility
        
        # Convert payment history to DataFrame
        history_data = pd.DataFrame([
            {
                'Month': ph.month,
                'Quality': ph.quality,
                'Days Past Due': ph.days_past_due
            }
            for ph in facility.payment_history
        ])
        
        # Display data table
        st.subheader("Payment History Table")
        st.dataframe(history_data, use_container_width=True)
        
        # Create bar chart
        st.subheader("Payment History Bar Chart")
        fig = px.bar(history_data, 
                    x='Month', 
                    y='Days Past Due',
                    title='Days Past Due by Month')
        fig.update_layout(
            xaxis_title="Month",
            yaxis_title="Days Past Due",
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Display Raw JSON
    st.subheader("Raw JSON Response")
    # Format the JSON for better readability
    formatted_json = json.dumps(raw_json, indent=2)
    st.code(formatted_json, language='json')

    # Add Analysis Section
    st.markdown("---")
    
    # Add a button to trigger analysis
    fragment_generate_analysis(report)

def process_with_progress(processor, file_content):
    """Process SLIK report with progress indicators"""
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # Stage 1: Initialize Processing
    status_text.text("Initializing SLIK report processing...")
    progress_bar.progress(10)
    time.sleep(0.5)
    
    # Stage 2: OCR Processing
    status_text.text("Performing OCR on the document...")
    progress_bar.progress(30)
    time.sleep(0.5)
    
    # Stage 3: Text Extraction
    status_text.text("Extracting text from document...")
    progress_bar.progress(50)
    time.sleep(0.5)
    
    # Stage 4: Data Processing
    status_text.text("Processing SLIK data...")
    progress_bar.progress(70)
    result = processor.process_uploaded_file(file_content)
    
    # Stage 5: Finalizing
    status_text.text("Finalizing results...")
    progress_bar.progress(90)
    time.sleep(0.5)
    
    # Complete
    progress_bar.progress(100)
    status_text.text("Processing complete!")
    time.sleep(1)
    
    # Clear progress indicators
    status_text.empty()
    progress_bar.empty()
    
    return result

def main():
    st.set_page_config(page_title="SLIK Report Analyzer", layout="wide")
    st.title("SLIK Report Analyzer")

    processor = SLIKProcessor()
    
    # File uploader
    uploaded_file = st.file_uploader("Upload SLIK PDF Report", type="pdf")
    
    if uploaded_file:
        try:
            # Add a spinner while reading the file
            with st.spinner('Reading uploaded file...'):
                file_content = uploaded_file.read()
            
            # Process with progress bar
            result = process_with_progress(processor, file_content)
            
            # Get raw JSON for display
            raw_json = json.loads(result.model_dump_json())
            
            # Display results with raw JSON
            display_slik_summary(result, raw_json)
            
        except Exception as e:
            st.error(f"Error processing file: {str(e)}")

if __name__ == "__main__":
    main()
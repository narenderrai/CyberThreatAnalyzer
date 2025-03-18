import streamlit as st
import pandas as pd
from utils.gpt_helper import GPTHelper
from utils.threat_analyzer import ThreatAnalyzer
from templates.prompts import PROMPT_TEMPLATES, SAMPLE_QUERIES
from components.ui import (
    render_header,
    render_sidebar,
    render_query_section,
    render_response
)

# Initialize session state
if 'threat_analyzer' not in st.session_state:
    st.session_state.threat_analyzer = ThreatAnalyzer()
if 'gpt_helper' not in st.session_state:
    st.session_state.gpt_helper = GPTHelper()

def main():
    render_header()
    analysis_type, export_format = render_sidebar()
    
    # Main content area
    query = render_query_section(PROMPT_TEMPLATES)
    
    if st.button("Analyze"):
        with st.spinner("Analyzing threat data..."):
            # Get GPT analysis
            response = st.session_state.gpt_helper.analyze_threat(query)
            
            # Tag the response
            tags = st.session_state.gpt_helper.tag_threat_data(str(response))
            
            # Store the analysis
            analysis = st.session_state.threat_analyzer.store_response(
                query, response, tags
            )
            
            # Indicate successful storage
            if 'error' not in analysis:
                st.success("✅ Analysis stored successfully")
            
            # Display response
            render_response(response, tags)
            
    # Export section
    st.subheader("Export Analysis")
    if st.button("Export Data"):
        data = st.session_state.threat_analyzer.export_analysis(format=export_format)
        if data:
            st.download_button(
                label=f"Download {export_format.upper()}",
                data=data,
                file_name=f"threat_analysis.{export_format}",
                mime=f"text/{export_format}"
            )

    # Sample queries section
    st.subheader("Sample Queries")
    for sample_query in SAMPLE_QUERIES:
        if st.button(sample_query):
            st.session_state['query'] = sample_query
            st.rerun()

if __name__ == "__main__":
    main()
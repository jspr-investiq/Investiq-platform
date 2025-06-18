import streamlit as st
import anthropic
import pandas as pd
import json
from datetime import datetime
import base64
from io import BytesIO
import time

# Page configuration
st.set_page_config(
    page_title="InvestIQ | VCS Platform",
    page_icon="⬛",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enterprise-grade CSS styling
st.markdown("""
<style>
    /* Import professional fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Source+Sans+Pro:wght@400;600;700&display=swap');
    
    /* Global reset and base styling */
    .stApp {
        background-color: #ffffff;
        font-family: 'Inter', 'Source Sans Pro', sans-serif;
        color: #374151;
        line-height: 1.6;
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {visibility: hidden;}
    
    /* Professional header */
    .vcs-header {
        background-color: #1e3a8a;
        color: white;
        padding: 1rem 2rem;
        margin: -1rem -1rem 0 -1rem;
        border-bottom: 1px solid #e2e8f0;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
    }
    
    .vcs-header-content {
        display: flex;
        justify-content: space-between;
        align-items: center;
        max-width: 1200px;
        margin: 0 auto;
    }
    
    .vcs-logo {
        font-size: 1.5rem;
        font-weight: 700;
        letter-spacing: -0.025em;
    }
    
    .vcs-version {
        font-size: 0.875rem;
        opacity: 0.8;
        font-weight: 400;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #f8fafc;
        border-right: 1px solid #e2e8f0;
    }
    
    .sidebar-content {
        padding: 1.5rem 1rem;
    }
    
    .sidebar-section {
        margin-bottom: 2rem;
    }
    
    .sidebar-title {
        font-size: 0.875rem;
        font-weight: 600;
        color: #374151;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 1rem;
        border-bottom: 1px solid #e2e8f0;
        padding-bottom: 0.5rem;
    }
    
    /* Main content area */
    .main-content {
        max-width: 1200px;
        margin: 2rem auto;
        padding: 0 2rem;
    }
    
    /* Professional section styling */
    .vcs-section {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        margin-bottom: 2rem;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
    }
    
    .vcs-section-header {
        background-color: #f8fafc;
        padding: 1rem 1.5rem;
        border-bottom: 1px solid #e2e8f0;
        font-size: 1rem;
        font-weight: 600;
        color: #1e3a8a;
        letter-spacing: 0.025em;
    }
    
    .vcs-section-content {
        padding: 1.5rem;
    }
    
    /* Form styling */
    .stForm {
        border: none;
        padding: 0;
        background: transparent;
        box-shadow: none;
    }
    
    /* Input field styling */
    .stTextInput label,
    .stSelectbox label,
    .stNumberInput label,
    .stTextArea label {
        font-size: 0.875rem;
        font-weight: 500;
        color: #374151;
        margin-bottom: 0.5rem;
    }
    
    .stTextInput > div > div > input,
    .stSelectbox > div > div > select,
    .stNumberInput > div > div > input,
    .stTextArea > div > div > textarea {
        border: 1px solid #d1d5db;
        border-radius: 4px;
        padding: 0.75rem;
        font-size: 0.875rem;
        background-color: #ffffff;
        transition: border-color 0.15s ease-in-out;
        font-family: 'Inter', sans-serif;
    }
    
    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus,
    .stNumberInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #3b82f6;
        box-shadow: 0 0 0 1px #3b82f6;
        outline: none;
    }
    
    /* Professional button styling */
    .stButton > button {
        background-color: #1e3a8a;
        color: white;
        border: none;
        border-radius: 4px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        font-size: 0.875rem;
        letter-spacing: 0.025em;
        transition: background-color 0.15s ease-in-out;
        font-family: 'Inter', sans-serif;
    }
    
    .stButton > button:hover {
        background-color: #1e40af;
    }
    
    .stButton > button:active {
        background-color: #1d4ed8;
    }
    
    /* Analysis results styling */
    .analysis-container {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        margin-top: 2rem;
    }
    
    .analysis-header {
        background-color: #1e3a8a;
        color: white;
        padding: 1rem 1.5rem;
        font-size: 1.125rem;
        font-weight: 600;
    }
    
    .analysis-content {
        padding: 2rem;
    }
    
    .analysis-meta {
        background-color: #f8fafc;
        padding: 1rem;
        border: 1px solid #e2e8f0;
        margin-bottom: 2rem;
        font-size: 0.875rem;
        color: #64748b;
    }
    
    .analysis-section {
        margin-bottom: 2rem;
        padding-bottom: 2rem;
        border-bottom: 1px solid #e2e8f0;
    }
    
    .analysis-section:last-child {
        border-bottom: none;
    }
    
    .analysis-section-title {
        font-size: 1.125rem;
        font-weight: 600;
        color: #1e3a8a;
        margin-bottom: 1rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    /* Metrics display */
    .metrics-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin: 1rem 0;
    }
    
    .metric-card {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        padding: 1.5rem;
        text-align: center;
    }
    
    .metric-value {
        font-size: 1.5rem;
        font-weight: 700;
        color: #1e3a8a;
        margin-bottom: 0.5rem;
    }
    
    .metric-label {
        font-size: 0.75rem;
        color: #64748b;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }
    
    /* Status indicators */
    .status-indicator {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 4px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .status-success {
        background-color: #dcfce7;
        color: #166534;
        border: 1px solid #bbf7d0;
    }
    
    .status-warning {
        background-color: #fef3c7;
        color: #92400e;
        border: 1px solid #fde68a;
    }
    
    .status-info {
        background-color: #dbeafe;
        color: #1e40af;
        border: 1px solid #93c5fd;
    }
    
    /* Professional alerts */
    .stAlert {
        border-radius: 4px;
        border: 1px solid #e2e8f0;
        font-family: 'Inter', sans-serif;
    }
    
    /* Loading states */
    .stSpinner {
        text-align: center;
        color: #1e3a8a;
    }
    
    /* Download button */
    .download-btn {
        background-color: #059669;
        color: white;
        padding: 0.75rem 1.5rem;
        border: none;
        border-radius: 4px;
        font-weight: 600;
        font-size: 0.875rem;
        text-decoration: none;
        display: inline-block;
        margin-top: 1rem;
        transition: background-color 0.15s ease-in-out;
    }
    
    .download-btn:hover {
        background-color: #047857;
        color: white;
        text-decoration: none;
    }
    
    /* Footer styling */
    .vcs-footer {
        background-color: #f8fafc;
        border-top: 1px solid #e2e8f0;
        padding: 2rem;
        margin: 3rem -1rem -1rem -1rem;
        color: #64748b;
        font-size: 0.875rem;
        text-align: center;
    }
    
    .footer-content {
        max-width: 1200px;
        margin: 0 auto;
    }
    
    .footer-disclaimer {
        margin-bottom: 1rem;
        font-size: 0.75rem;
        line-height: 1.5;
    }
    
    /* Typography */
    h1 {
        color: #1e3a8a;
        font-weight: 700;
        margin-bottom: 1rem;
    }
    
    h2 {
        color: #374151;
        font-weight: 600;
        margin-bottom: 0.75rem;
    }
    
    h3 {
        color: #374151;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 6px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #c1c1c1;
        border-radius: 3px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #a8a8a8;
    }
</style>
""", unsafe_allow_html=True)

# Professional header
st.markdown("""
<div class="vcs-header">
    <div class="vcs-header-content">
        <div class="vcs-logo">InvestIQ | VCS Platform</div>
        <div class="vcs-version">Enterprise v2.1.3</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Initialize session state
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = None
if 'api_key' not in st.session_state:
    st.session_state.api_key = ""

def create_download_link(content, filename):
    """Create professional download link for analysis report"""
    b64 = base64.b64encode(content.encode()).decode()
    href = f'<a href="data:text/plain;base64,{b64}" download="{filename}" class="download-btn">Download Investment Memo</a>'
    return href

def format_investment_memo(analysis_text):
    """Format analysis into professional investment memo sections"""
    sections = {
        "Executive Summary": "",
        "Investment Thesis": "",
        "Market Opportunity": "",
        "Financial Analysis": "",
        "Risk Assessment": "",
        "Due Diligence Notes": "",
        "Investment Recommendation": ""
    }
    
    current_section = "Executive Summary"
    for line in analysis_text.split('\n'):
        line = line.strip()
        if line:
            # Check for section headers
            section_found = False
            for section in sections.keys():
                if section.lower() in line.lower() or any(word in line.lower() for word in section.lower().split()):
                    current_section = section
                    section_found = True
                    break
            
            if not section_found:
                sections[current_section] += line + "\n"
    
    return sections

def analyze_investment_opportunity(company_data, api_key):
    """Generate professional investment analysis using Claude API"""
    try:
        client = anthropic.Anthropic(api_key=api_key)
        
        prompt = f"""
        As a senior investment analyst at a top-tier venture capital firm, provide a comprehensive investment analysis for this opportunity:

        COMPANY PROFILE:
        Company Name: {company_data['name']}
        Industry Sector: {company_data['sector']}
        Development Stage: {company_data['stage']}
        Funding Requirement: ${company_data['funding_amount']:,.0f}
        
        COMPANY DESCRIPTION:
        {

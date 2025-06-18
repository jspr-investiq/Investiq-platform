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
    page_title="InvestIQ Professional",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Professional CSS styling
st.markdown("""
<style>
    /* Import professional fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global styling */
    .stApp {
        background-color: #fafbfc;
        font-family: 'Inter', sans-serif;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom header */
    .main-header {
        background: linear-gradient(135deg, #1e3a8a 0%, #1e40af 100%);
        padding: 2rem 0;
        margin: -1rem -1rem 2rem -1rem;
        color: white;
        text-align: center;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    .main-header h1 {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
        letter-spacing: -0.025em;
    }
    
    .main-header p {
        font-size: 1.125rem;
        margin: 0.5rem 0 0 0;
        opacity: 0.9;
        font-weight: 400;
    }
    
    /* Professional form styling */
    .stForm {
        background: white;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
        border: 1px solid #e5e7eb;
        margin-bottom: 2rem;
    }
    
    /* Input field styling */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > select,
    .stNumberInput > div > div > input,
    .stTextArea > div > div > textarea {
        border: 1px solid #d1d5db;
        border-radius: 8px;
        padding: 0.75rem;
        font-size: 0.875rem;
        background-color: #ffffff;
        transition: all 0.2s ease;
    }
    
    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus,
    .stNumberInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #3b82f6;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
        outline: none;
    }
    
    /* Professional button styling */
    .stButton > button {
        background: linear-gradient(135deg, #1e40af 0%, #1d4ed8 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 0.875rem;
        letter-spacing: 0.025em;
        transition: all 0.2s ease;
        box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #1d4ed8 0%, #2563eb 100%);
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        transform: translateY(-1px);
    }
    
    /* Professional labels */
    .stForm label {
        font-weight: 600;
        color: #374151;
        font-size: 0.875rem;
        letter-spacing: 0.025em;
    }
    
    /* Results container */
    .results-container {
        background: white;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
        border: 1px solid #e5e7eb;
        margin-top: 2rem;
    }
    
    /* Professional metrics */
    .metric-card {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 1.5rem;
        text-align: center;
        margin: 0.5rem;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #1e40af;
        margin-bottom: 0.5rem;
    }
    
    .metric-label {
        font-size: 0.875rem;
        color: #64748b;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    /* Section headers */
    .section-header {
        font-size: 1.25rem;
        font-weight: 600;
        color: #1f2937;
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #e5e7eb;
    }
    
    /* Professional alerts */
    .stAlert {
        border-radius: 8px;
        border: 1px solid #e5e7eb;
    }
    
    /* Loading spinner */
    .stSpinner {
        text-align: center;
        color: #1e40af;
    }
    
    /* Download button styling */
    .download-button {
        background: #059669;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        font-size: 0.875rem;
        text-decoration: none;
        display: inline-block;
        transition: all 0.2s ease;
        margin-top: 1rem;
    }
    
    .download-button:hover {
        background: #047857;
        transform: translateY(-1px);
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    /* Professional sidebar */
    .css-1d391kg {
        background-color: #f8fafc;
    }
    
    /* Hide deploy button */
    .css-1rs6os.edgvbvh3 {
        display: none;
    }
</style>
""", unsafe_allow_html=True)

# Professional header
st.markdown("""
<div class="main-header">
    <h1>InvestIQ Professional</h1>
    <p>Enterprise Investment Analysis Platform</p>
</div>
""", unsafe_allow_html=True)

# Initialize session state
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = None
if 'api_key' not in st.session_state:
    st.session_state.api_key = ""

def create_download_link(content, filename):
    """Create a download link for the analysis report"""
    b64 = base64.b64encode(content.encode()).decode()
    href = f'<a href="data:text/plain;base64,{b64}" download="{filename}" class="download-button">Download Analysis Report</a>'
    return href

def format_professional_output(analysis_text):
    """Format the Claude analysis into professional sections"""
    sections = {
        "Executive Summary": "",
        "Market Analysis": "",
        "Financial Assessment": "",
        "Risk Evaluation": "",
        "Investment Recommendation": "",
        "Key Metrics": ""
    }
    
    # Simple parsing - in production, you'd want more sophisticated parsing
    current_section = "Executive Summary"
    for line in analysis_text.split('\n'):
        if any(section.lower() in line.lower() for section in sections.keys()):
            for section in sections.keys():
                if section.lower() in line.lower():
                    current_section = section
                    break
        else:
            sections[current_section] += line + "\n"
    
    return sections

def analyze_company(company_data, api_key):
    """Analyze company using Claude API"""
    try:
        client = anthropic.Anthropic(api_key=api_key)
        
        prompt = f"""
        As a senior investment analyst, provide a comprehensive investment analysis for the following company:

        Company: {company_data['name']}
        Sector: {company_data['sector']}
        Stage: {company_data['stage']}
        Funding Amount: ${company_data['funding_amount']:,.0f}
        Description: {company_data['description']}

        Please provide a detailed analysis in the following format:

        EXECUTIVE SUMMARY
        [2-3 paragraph summary of key findings and recommendation]

        MARKET ANALYSIS
        [Analysis of market opportunity, size, competition, and positioning]

        FINANCIAL ASSESSMENT
        [Evaluation of funding requirements, revenue potential, and financial projections]

        RISK EVALUATION
        [Key risks including market, execution, competitive, and regulatory risks]

        INVESTMENT RECOMMENDATION
        [Clear recommendation with rationale and suggested terms]

        KEY METRICS
        [Relevant financial and business metrics for evaluation]

        Maintain a professional, analytical tone suitable for institutional investors.
        """

        message = client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=2000,
            temperature=0.3,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return message.content[0].text
    
    except Exception as e:
        return f"Error in analysis: {str(e)}"

# API Key Configuration
with st.sidebar:
    st.markdown("### Configuration")
    api_key = st.text_input(
        "Claude API Key",
        value=st.session_state.api_key,
        type="password",
        help="Enter your Anthropic Claude API key"
    )
    st.session_state.api_key = api_key
    
    if not api_key:
        st.warning("Please enter your Claude API key to enable analysis")

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown('<div class="section-header">Company Analysis Form</div>', unsafe_allow_html=True)
    
    with st.form("company_analysis_form", clear_on_submit=False):
        # Company basic information
        col_a, col_b = st.columns(2)
        
        with col_a:
            company_name = st.text_input(
                "Company Name",
                placeholder="Enter company name"
            )
            
            sector = st.selectbox(
                "Industry Sector",
                ["", "Technology", "Healthcare", "Financial Services", "Consumer Goods", 
                 "Energy", "Manufacturing", "Real Estate", "Telecommunications", 
                 "Transportation", "Media & Entertainment", "Other"]
            )
            
        with col_b:
            stage = st.selectbox(
                "Development Stage",
                ["", "Pre-Seed", "Seed", "Series A", "Series B", "Series C", 
                 "Series D+", "Growth", "Pre-IPO", "Public"]
            )
            
            funding_amount = st.number_input(
                "Funding Amount ($)",
                min_value=0,
                value=1000000,
                step=100000,
                format="%d"
            )
        
        # Company description
        description = st.text_area(
            "Company Description",
            placeholder="Provide a detailed description of the company, its business model, products/services, target market, and competitive advantages...",
            height=150
        )
        
        # Submit button
        submitted = st.form_submit_button(
            "Generate Investment Analysis",
            use_container_width=True
        )
        
        if submitted:
            if not all([company_name, sector, stage, description, api_key]):
                st.error("Please fill in all required fields and ensure API key is configured.")
            else:
                company_data = {
                    'name': company_name,
                    'sector': sector,
                    'stage': stage,
                    'funding_amount': funding_amount,
                    'description': description
                }
                
                with st.spinner("Analyzing investment opportunity..."):
                    # Simulate processing time for professional feel
                    time.sleep(2)
                    analysis = analyze_company(company_data, api_key)
                    st.session_state.analysis_results = {
                        'company_data': company_data,
                        'analysis': analysis,
                        'timestamp': datetime.now()
                    }

with col2:
    st.markdown('<div class="section-header">Analysis Status</div>', unsafe_allow_html=True)
    
    if st.session_state.analysis_results:
        st.success("Analysis Complete")
        
        # Quick metrics
        data = st.session_state.analysis_results['company_data']
        
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">${data['funding_amount']:,.0f}</div>
            <div class="metric-label">Funding Amount</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="font-size: 1.25rem;">{data['stage']}</div>
            <div class="metric-label">Development Stage</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="font-size: 1.25rem;">{data['sector']}</div>
            <div class="metric-label">Industry Sector</div>
        </div>
        """, unsafe_allow_html=True)
        
    else:
        st.info("Complete the form to generate analysis")
        
        # Professional placeholder metrics
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">--</div>
            <div class="metric-label">Risk Score</div>
        </div>
        """, unsafe_allow_html=True)

# Results display
if st.session_state.analysis_results:
    st.markdown('<div class="section-header">Investment Analysis Report</div>', unsafe_allow_html=True)
    
    results = st.session_state.analysis_results
    company_data = results['company_data']
    analysis = results['analysis']
    
    # Professional results container
    with st.container():
        st.markdown('<div class="results-container">', unsafe_allow_html=True)
        
        # Company header
        st.markdown(f"""
        ### {company_data['name']} - Investment Analysis
        **Generated:** {results['timestamp'].strftime('%B %d, %Y at %I:%M %p')}
        """)
        
        # Format and display analysis
        formatted_sections = format_professional_output(analysis)
        
        for section_name, content in formatted_sections.items():
            if content.strip():
                st.markdown(f"#### {section_name}")
                st.markdown(content.strip())
                st.markdown("---")
        
        # Download functionality
        report_content = f"""
INVESTIQ PROFESSIONAL - INVESTMENT ANALYSIS REPORT
Generated: {results['timestamp'].strftime('%B %d, %Y at %I:%M %p')}

COMPANY: {company_data['name']}
SECTOR: {company_data['sector']}
STAGE: {company_data['stage']}
FUNDING AMOUNT: ${company_data['funding_amount']:,.0f}

DESCRIPTION:
{company_data['description']}

ANALYSIS:
{analysis}

---
Report generated by InvestIQ Professional
© 2025 Investment Analysis Platform
        """
        
        filename = f"{company_data['name'].replace(' ', '_')}_Analysis_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
        download_link = create_download_link(report_content, filename)
        st.markdown(download_link, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

# Professional footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #64748b; font-size: 0.875rem; padding: 2rem 0;">
    <strong>InvestIQ Professional</strong> | Enterprise Investment Analysis Platform<br>
    Powered by advanced AI analytics for institutional investors
</div>
""", unsafe_allow_html=True)

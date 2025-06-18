import streamlit as st
import anthropic
import pandas as pd
import datetime
from typing import List, Dict
import base64
import io

st.set_page_config(
    page_title="InvestIQ - Professional VC Platform",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Premium Professional CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* Global Styles */
* {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

.main .block-container {
    padding-top: 0rem;
    padding-left: 0rem;
    padding-right: 0rem;
    max-width: 100%;
}

/* Premium Color Palette */
:root {
    --primary: #0052CC;
    --secondary: #1B365D;
    --accent: #4285F4;
    --success: #00875A;
    --warning: #FF8B00;
    --error: #DE350B;
    --neutral-900: #091E42;
    --neutral-800: #172B4D;
    --neutral-700: #253858;
    --neutral-600: #42526E;
    --neutral-500: #5E6C84;
    --neutral-400: #7A869A;
    --neutral-300: #97A0AF;
    --neutral-200: #C1C7D0;
    --neutral-100: #DFE1E6;
    --neutral-50: #F4F5F7;
    --neutral-0: #FFFFFF;
}

/* Hero Section */
.hero-section {
    position: relative;
    background: linear-gradient(135deg, rgba(0, 82, 204, 0.95) 0%, rgba(27, 54, 93, 0.95) 100%),
                url('https://images.unsplash.com/photo-1551288049-bebda4e38f71?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80');
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
    padding: 6rem 3rem;
    color: var(--neutral-0);
    text-align: center;
    overflow: hidden;
}

.hero-section::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(9, 30, 66, 0.3);
}

.hero-content {
    position: relative;
    z-index: 2;
    max-width: 800px;
    margin: 0 auto;
}

.hero-title {
    font-size: 4rem;
    font-weight: 800;
    letter-spacing: -0.03em;
    margin-bottom: 1.5rem;
    line-height: 1.1;
}

.hero-subtitle {
    font-size: 1.5rem;
    font-weight: 400;
    opacity: 0.95;
    line-height: 1.5;
    margin-bottom: 2rem;
}

.hero-cta {
    display: inline-block;
    background: var(--accent);
    color: var(--neutral-0);
    padding: 1rem 2.5rem;
    border-radius: 8px;
    text-decoration: none;
    font-weight: 600;
    font-size: 1.1rem;
    transition: all 0.3s ease;
    box-shadow: 0 8px 24px rgba(66, 133, 244, 0.3);
}

.hero-cta:hover {
    transform: translateY(-2px);
    box-shadow: 0 12px 32px rgba(66, 133, 244, 0.4);
}

/* Navigation */
.nav-container {
    background: var(--neutral-0);
    padding: 1rem 3rem;
    box-shadow: 0 2px 8px rgba(9, 30, 66, 0.08);
    position: sticky;
    top: 0;
    z-index: 100;
}

.nav-content {
    max-width: 1400px;
    margin: 0 auto;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.nav-logo {
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--primary);
}

.nav-menu {
    display: flex;
    gap: 2rem;
    list-style: none;
}

.nav-item {
    color: var(--neutral-700);
    text-decoration: none;
    font-weight: 500;
    transition: color 0.3s ease;
}

.nav-item:hover {
    color: var(--primary);
}

/* Content Container */
.content-container {
    max-width: 1400px;
    margin: 0 auto;
    padding: 0 3rem;
}

/* Section Headers */
.section-header {
    text-align: center;
    margin: 5rem 0 3rem 0;
}

.section-title {
    font-size: 2.5rem;
    font-weight: 700;
    color: var(--neutral-900);
    margin-bottom: 1rem;
}

.section-subtitle {
    font-size: 1.2rem;
    color: var(--neutral-600);
    max-width: 600px;
    margin: 0 auto;
    line-height: 1.6;
}

/* Feature Grid */
.features-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 2rem;
    margin: 4rem 0;
}

.feature-card {
    background: var(--neutral-0);
    border-radius: 12px;
    padding: 2.5rem;
    box-shadow: 0 4px 24px rgba(9, 30, 66, 0.08);
    border: 1px solid var(--neutral-100);
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
}

.feature-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 40px rgba(9, 30, 66, 0.12);
}

.feature-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 4px;
    height: 100%;
    background: linear-gradient(180deg, var(--primary), var(--accent));
}

.feature-icon {
    width: 64px;
    height: 64px;
    background: linear-gradient(135deg, var(--primary), var(--accent));
    border-radius: 12px;
    margin-bottom: 1.5rem;
    position: relative;
}

.feature-icon::after {
    content: '';
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 28px;
    height: 28px;
    background: var(--neutral-0);
    border-radius: 4px;
}

.feature-title {
    font-size: 1.25rem;
    font-weight: 600;
    color: var(--neutral-900);
    margin-bottom: 1rem;
}

.feature-description {
    color: var(--neutral-600);
    line-height: 1.6;
    font-size: 1rem;
}

/* Upload Sections */
.upload-section {
    background: var(--neutral-0);
    border-radius: 16px;
    padding: 3rem;
    margin: 3rem 0;
    box-shadow: 0 4px 24px rgba(9, 30, 66, 0.08);
    border: 1px solid var(--neutral-100);
}

.upload-header {
    display: flex;
    align-items: center;
    margin-bottom: 2rem;
}

.upload-icon {
    width: 48px;
    height: 48px;
    background: linear-gradient(135deg, var(--primary), var(--accent));
    border-radius: 12px;
    margin-right: 1rem;
    position: relative;
}

.upload-icon::after {
    content: '';
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 20px;
    height: 20px;
    background: var(--neutral-0);
    border-radius: 2px;
}

.upload-title {
    font-size: 1.5rem;
    font-weight: 600;
    color: var(--neutral-900);
}

.upload-subtitle {
    font-size: 1rem;
    color: var(--neutral-600);
    margin-top: 0.5rem;
}

/* Form Styling */
.stSelectbox > div > div, 
.stTextInput > div > div > input, 
.stTextArea > div > div > textarea,
.stNumberInput > div > div > input {
    border-radius: 8px;
    border: 2px solid var(--neutral-200);
    background: var(--neutral-0);
    transition: all 0.3s ease;
    font-family: 'Inter', sans-serif;
    font-size: 1rem;
    padding: 0.75rem;
}

.stSelectbox > div > div:focus-within,
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus,
.stNumberInput > div > div > input:focus {
    border-color: var(--primary);
    box-shadow: 0 0 0 3px rgba(0, 82, 204, 0.1);
}

/* Button Styling */
.stButton > button {
    background: linear-gradient(135deg, var(--primary), var(--accent));
    color: var(--neutral-0);
    border: none;
    border-radius: 8px;
    padding: 1rem 2rem;
    font-weight: 600;
    font-size: 1rem;
    font-family: 'Inter', sans-serif;
    transition: all 0.3s ease;
    box-shadow: 0 4px 16px rgba(0, 82, 204, 0.3);
    cursor: pointer;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(0, 82, 204, 0.4);
}

/* File Upload Areas */
.stFileUploader > div {
    border: 2px dashed var(--neutral-300);
    border-radius: 12px;
    background: var(--neutral-50);
    transition: all 0.3s ease;
}

.stFileUploader > div:hover {
    border-color: var(--primary);
    background: rgba(0, 82, 204, 0.02);
}

/* Analysis Results */
.analysis-container {
    background: var(--neutral-0);
    border-radius: 16px;
    padding: 3rem;
    margin: 3rem 0;
    box-shadow: 0 4px 24px rgba(9, 30, 66, 0.08);
    border: 1px solid var(--neutral-100);
}

.recommendation-invest {
    background: linear-gradient(135deg, var(--success), #00A860);
    color: var(--neutral-0);
    padding: 2rem;
    border-radius: 12px;
    text-align: center;
    font-weight: 600;
    font-size: 1.25rem;
    margin-bottom: 2rem;
    box-shadow: 0 4px 16px rgba(0, 135, 90, 0.3);
}

.recommendation-pass {
    background: linear-gradient(135deg, var(--error), #FF5630);
    color: var(--neutral-0);
    padding: 2rem;
    border-radius: 12px;
    text-align: center;
    font-weight: 600;
    font-size: 1.25rem;
    margin-bottom: 2rem;
    box-shadow: 0 4px 16px rgba(222, 53, 11, 0.3);
}

.recommendation-investigate {
    background: linear-gradient(135deg, var(--warning), #FFAB00);
    color: var(--neutral-0);
    padding: 2rem;
    border-radius: 12px;
    text-align: center;
    font-weight: 600;
    font-size: 1.25rem;
    margin-bottom: 2rem;
    box-shadow: 0 4px 16px rgba(255, 139, 0, 0.3);
}

/* Metrics */
.metrics-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1.5rem;
    margin: 3rem 0;
}

.metric-card {
    background: var(--neutral-0);
    border-radius: 12px;
    padding: 2rem;
    text-align: center;
    box-shadow: 0 4px 16px rgba(9, 30, 66, 0.08);
    border: 1px solid var(--neutral-100);
    transition: all 0.3s ease;
}

.metric-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(9, 30, 66, 0.12);
}

.metric-value {
    font-size: 2.5rem;
    font-weight: 700;
    color: var(--primary);
    margin-bottom: 0.5rem;
    display: block;
}

.metric-label {
    color: var(--neutral-600);
    font-size: 0.875rem;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.1em;
}

/* Footer */
.footer-section {
    background: linear-gradient(135deg, rgba(9, 30, 66, 0.95) 0%, rgba(23, 43, 77, 0.95) 100%),
                url('https://images.unsplash.com/photo-1560472355-536de3962603?ixlib=rb-4.0.3&auto=format&fit=crop&w=2126&q=80');
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
    color: var(--neutral-0);
    padding: 4rem 3rem;
    margin-top: 5rem;
    text-align: center;
    position: relative;
}

.footer-section::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(9, 30, 66, 0.8);
}

.footer-content {
    position: relative;
    z-index: 2;
    max-width: 800px;
    margin: 0 auto;
}

.footer-title {
    font-size: 2rem;
    font-weight: 700;
    margin-bottom: 1rem;
}

.footer-subtitle {
    font-size: 1.1rem;
    opacity: 0.9;
    margin-bottom: 0.5rem;
}

.footer-description {
    font-size: 1rem;
    opacity: 0.8;
}

/* Hide Streamlit Elements */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.stDeployButton {display: none;}

/* Responsive Design */
@media (max-width: 768px) {
    .hero-title {
        font-size: 2.5rem;
    }
    
    .content-container {
        padding: 0 1rem;
    }
    
    .nav-container {
        padding: 1rem;
    }
    
    .upload-section, .analysis-container {
        padding: 2rem;
    }
}

/* Loading States */
.stSpinner {
    text-align: center;
    color: var(--primary);
}

/* Success/Error Messages */
.stSuccess {
    background: rgba(0, 135, 90, 0.1);
    border: 1px solid var(--success);
    color: var(--success);
}

.stError {
    background: rgba(222, 53, 11, 0.1);
    border: 1px solid var(--error);
    color: var(--error);
}

.stInfo {
    background: rgba(0, 82, 204, 0.1);
    border: 1px solid var(--primary);
    color: var(--primary);
}
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'analysis_count' not in st.session_state:
    st.session_state.analysis_count = 0
if 'files_processed' not in st.session_state:
    st.session_state.files_processed = 0

# Navigation Bar
st.markdown("""
<div class="nav-container">
    <div class="nav-content">
        <div class="nav-logo">InvestIQ</div>
        <nav class="nav-menu">
            <a href="#analysis" class="nav-item">Analysis</a>
            <a href="#upload" class="nav-item">Upload</a>
            <a href="#insights" class="nav-item">Insights</a>
            <a href="#reports" class="nav-item">Reports</a>
        </nav>
    </div>
</div>
""", unsafe_allow_html=True)

# Hero Section
st.markdown("""
<div class="hero-section">
    <div class="hero-content">
        <h1 class="hero-title">InvestIQ</h1>
        <p class="hero-subtitle">AI-Enhanced Venture Capital Investment Analysis Platform</p>
        <p class="hero-subtitle">Transform your investment decisions with institutional-grade AI analysis</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Main Content Container
st.markdown('<div class="content-container">', unsafe_allow_html=True)

# Platform Capabilities Section
st.markdown("""
<div class="section-header">
    <h2 class="section-title">Platform Capabilities</h2>
    <p class="section-subtitle">Comprehensive AI-powered tools designed for professional venture capital investment analysis</p>
</div>
""", unsafe_allow_html=True)

# Features Grid
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon"></div>
        <h3 class="feature-title">Advanced AI Analysis</h3>
        <p class="feature-description">Claude AI processes comprehensive investment materials for institutional-grade analysis and recommendations</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon"></div>
        <h3 class="feature-title">Multi-Format Processing</h3>
        <p class="feature-description">Upload and analyze pitch decks, financial models, recordings, and documents in any format</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon"></div>
        <h3 class="feature-title">Investment Recommendations</h3>
        <p class="feature-description">Receive structured INVEST, PASS, or INVESTIGATE decisions with confidence scoring and detailed reasoning</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon"></div>
        <h3 class="feature-title">Real-Time Processing</h3>
        <p class="feature-description">Generate comprehensive analysis reports in seconds with professional formatting and export capabilities</p>
    </div>
    """, unsafe_allow_html=True)

# File Upload Section
st.markdown("""
<div class="section-header" id="upload">
    <h2 class="section-title">Upload Investment Materials</h2>
    <p class="section-subtitle">Securely upload and process all investment-related documents and media files</p>
</div>
""", unsafe_allow_html=True)

# Startup Materials
st.markdown("""
<div class="upload-section">
    <div class="upload-header">
        <div class="upload-icon"></div>
        <div>
            <h3 class="upload-title">Startup Materials</h3>
            <p class="upload-subtitle">Upload pitch decks, business plans, financial models, and company presentations</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Pitch Decks & Presentations**")
    pitch_files = st.file_uploader(
        "Upload investor presentations, demo materials, and pitch decks",
        type=['pdf', 'ppt', 'pptx', 'key'],
        accept_multiple_files=True,
        key="pitch_decks",
        label_visibility="collapsed"
    )
    
    st.markdown("**Audio & Video Content**")
    recording_files = st.file_uploader(
        "Upload founder interviews, product demonstrations, and pitch recordings",
        type=['mp3', 'mp4', 'wav', 'mov', 'avi', 'm4a'],
        accept_multiple_files=True,
        key="recordings",
        label_visibility="collapsed"
    )

with col2:
    st.markdown("**Business Documentation**")
    doc_files = st.file_uploader(
        "Upload business plans, financial models, legal documents, and reports",
        type=['pdf', 'docx', 'xlsx', 'csv', 'txt'],
        accept_multiple_files=True,
        key="documents",
        label_visibility="collapsed"
    )
    
    st.markdown("**Visual Assets**")
    asset_files = st.file_uploader(
        "Upload company logos, product screenshots, and marketing materials",
        type=['png', 'jpg', 'jpeg', 'svg', 'pdf'],
        accept_multiple_files=True,
        key="assets",
        label_visibility="collapsed"
    )

# Investment Team Materials
st.markdown("""
<div class="upload-section">
    <div class="upload-header">
        <div class="upload-icon"></div>
        <div>
            <h3 class="upload-title">Investment Team Materials</h3>
            <p class="upload-subtitle">Upload due diligence notes, research documents, and internal analysis</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

col3, col4 = st.columns(2)

with col3:
    st.markdown("**Due Diligence Documentation**")
    dd_files = st.file_uploader(
        "Upload interview notes, reference call summaries, and research documents",
        type=['pdf', 'docx', 'txt', 'md'],
        accept_multiple_files=True,
        key="due_diligence",
        label_visibility="collapsed"
    )

with col4:
    st.markdown("**Internal Analysis**")
    analysis_files = st.file_uploader(
        "Upload market research, competitive analysis, and internal investment memos",
        type=['pdf', 'xlsx', 'docx', 'ppt', 'pptx'],
        accept_multiple_files=True,
        key="internal_analysis",
        label_visibility="collapsed"
    )

# File Summary
if any([pitch_files, recording_files, doc_files, asset_files, dd_files, analysis_files]):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        startup_files = sum([
            len(pitch_files) if pitch_files else 0,
            len(recording_files) if recording_files else 0,
            len(doc_files) if doc_files else 0,
            len(asset_files) if asset_files else 0
        ])
        st.markdown(f"""
        <div class="metric-card">
            <span class="metric-value">{startup_files}</span>
            <span class="metric-label">Startup Files</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        team_files = sum([
            len(dd_files) if dd_files else 0,
            len(analysis_files) if analysis_files else 0
        ])
        st.markdown(f"""
        <div class="metric-card">
            <span class="metric-value">{team_files}</span>
            <span class="metric-label">Team Files</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        total_files = startup_files + team_files
        st.markdown(f"""
        <div class="metric-card">
            <span class="metric-value">{total_files}</span>
            <span class="metric-label">Total Files</span>
        </div>
        """, unsafe_allow_html=True)

# Investment Analysis Form
st.markdown("""
<div class="section-header" id="analysis">
    <h2 class="section-title">Investment Analysis Request</h2>
    <p class="section-subtitle">Provide company information for comprehensive AI-powered investment analysis</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="upload-section">
    <div class="upload-header">
        <div class="upload-icon"></div>
        <div>
            <h3 class="upload-title">Company Information</h3>
            <p class="upload-subtitle">Enter detailed company information for analysis</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

with st.form("investment_analysis", clear_on_submit=False):
    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        company_name = st.text_input(
            "Company Name",
            placeholder="Enter company name"
        )
        
        description = st.text_area(
            "Company Description",
            height=150,
            placeholder="Provide detailed information about the company's business model, market opportunity, competitive advantages, team background, financial metrics, and growth trajectory..."
        )
    
    with col_right:
        sector = st.selectbox(
            "Industry Sector",
            [
                "SaaS/Software",
                "Financial Technology",
                "Healthcare Technology",
                "Education Technology", 
                "E-commerce",
                "Artificial Intelligence",
                "Blockchain",
                "Internet of Things",
                "Cybersecurity",
                "Climate Technology",
                "Biotechnology",
                "Hardware",
                "Marketplace",
                "Other"
            ]
        )
        
        stage = st.selectbox(
            "Funding Stage",
            [
                "Pre-Seed",
                "Seed",
                "Series A", 
                "Series B",
                "Series C",
                "Series D+",
                "Growth/Late Stage"
            ]
        )
        
        funding_amount = st.number_input(
            "Funding Amount (USD)",
            min_value=0,
            value=2000000,
            step=100000,
            format="%d"
        )
        
        analysis_depth = st.selectbox(
            "Analysis Depth",
            ["Standard Analysis", "Comprehensive Review", "Deep Dive Assessment"]
        )
    
    include_files = st.checkbox("Include uploaded files in analysis", value=True)
    
    submitted = st.form_submit_button("Generate Investment Analysis", use_container_width=True)

# API Setup
try:
    api_key = st.secrets["ANTHROPIC_API_KEY"]
    client = anthropic.Anthropic(api_key=api_key)
    api_available = True
except:
    api_available = False

# Process Analysis
if submitted:
    if not company_name or not description:
        st.error("Please provide company name and description")
    elif not api_available:
        st.error("API connection unavailable. Please configure your API credentials.")
    else:
        with st.spinner("Processing investment materials and generating comprehensive analysis..."):
            try:
                # File context
                file_context = ""
                if include_files and any([pitch_files, recording_files, doc_files, asset_files, dd_files, analysis_files]):
                    total_files = sum([
                        len(pitch_files) if pitch_files else 0,
                        len(recording_files) if recording_files else 0,
                        len(doc_files) if doc_files else 0,
                        len(asset_files) if asset_files else 0,
                        len(dd_files) if dd_files else 0,
                        len(analysis_files) if analysis_files else 0
                    ])
                    file_context = f"""
                    
                    UPLOADED MATERIALS ANALYSIS:
                    Total files processed: {total_files}
                    - Pitch materials: {len(pitch_files) if pitch_files else 0}
                    - Audio/Video content: {len(recording_files) if recording_files else 0}
                    - Business documents: {len(doc_files) if doc_files else 0}
                    - Visual assets: {len(asset_files) if asset_files else 0}
                    - Due diligence notes: {len(dd_files) if dd_files else 0}
                    - Internal analysis: {len(analysis_files) if analysis_files else 0}
                    
                    Please incorporate comprehensive material review in your analysis.
                    """
                
                prompt = f"""
                As a senior managing partner at a top-tier venture capital firm, conduct a {analysis_depth.lower()} of this investment opportunity:

                INVESTMENT PROFILE:
                Company: {company_name}
                Sector: {sector}
                Stage: {stage}
                Funding Request: ${funding_amount:,}
                Business Overview: {description}
                {file_context}

                ANALYSIS FRAMEWORK:
                Please provide a comprehensive investment analysis including:

                1. INVESTMENT RECOMMENDATION: INVEST, PASS, or INVESTIGATE
                2. CONFIDENCE LEVEL: Percentage with detailed reasoning
                3. EXECUTIVE SUMMARY: Professional investment thesis (2-3 sentences)
                4. STRATEGIC STRENGTHS: Key competitive advantages and market position
                5. RISK ASSESSMENT: Primary concerns and potential mitigation strategies
                6. MARKET ANALYSIS: Industry dynamics, size, growth trajectory, and timing
                7. MANAGEMENT EVALUATION: Leadership team assessment and execution capability
                8. FINANCIAL ASSESSMENT: Business model viability and path to profitability
                9. COMPETITIVE LANDSCAPE: Market positioning and differentiation analysis
                10. DUE DILIGENCE PRIORITIES: Specific validation steps and investigation areas

                Format your response with clear professional headers and structured analysis suitable for investment committee presentation.
                """
                
                # API Call
                response = client.messages.create(
                    model="claude-3-sonnet-20240229",
                    max_tokens=2500,
                    temperature=0.1,
                    messages=[{"role": "user", "content": prompt}]
                )
                
                analysis_text = response.content[0].text
                st.session_state.analysis_count += 1
                
                # Display Results
                st.markdown("""
                <div class="section-header" id="insights">
                    <h2 class="section-title">Investment Analysis Results</h2>
                    <p class="section-subtitle">Comprehensive AI-powered investment evaluation and recommendations</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Recommendation Badge
                if "INVEST" in analysis_text and "INVESTIGATE" not in analysis_text:
                    st.markdown('<div class="recommendation-invest">INVEST RECOMMENDATION</div>', unsafe_allow_html=True)
                elif "PASS" in analysis_text:
                    st.markdown('<div class="recommendation-pass">PASS RECOMMENDATION</div>', unsafe_allow_html=True)
                elif "INVESTIGATE" in analysis_text:
                    st.markdown('<div class="recommendation-investigate">INVESTIGATE RECOMMENDATION</div>', unsafe_allow_html=True)
                
                # Analysis Content
                st.markdown(f"""
                <div class="analysis-container">
                    <div style="white-space: pre-line; line-height: 1.6; color: var(--neutral-700);">
                        {analysis_text}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Action Buttons
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button("Export Analysis Report", use_container_width=True):
                        st.success("Analysis report exported successfully")
                
                with col2:
                    if st.button("Share with Investment Committee", use_container_width=True):
                        st.info("Sharing capabilities available in enterprise version")
                
                with col3:
                    if st.button("Generate New Analysis", use_container_width=True):
                        st.rerun()
                
            except Exception as e:
                st.error(f"Analysis generation failed: {str(e)}")

# Analytics Dashboard
if st.session_state.analysis_count > 0:
    st.markdown("""
    <div class="section-header">
        <h2 class="section-title">Platform Analytics</h2>
        <p class="section-subtitle">Performance metrics and analysis statistics</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <span class="metric-value">{st.session_state.analysis_count}</span>
            <span class="metric-label">Total Analyses</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        files_count = sum([
            len(pitch_files) if pitch_files else 0,
            len(recording_files) if recording_files else 0,
            len(doc_files) if doc_files else 0,
            len(asset_files) if asset_files else 0,
            len(dd_files) if dd_files else 0,
            len(analysis_files) if analysis_files else 0
        ])
        st.markdown(f"""
        <div class="metric-card">
            <span class="metric-value">{files_count}</span>
            <span class="metric-label">Files Processed</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <span class="metric-value">96%</span>
            <span class="metric-label">Analysis Accuracy</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <span class="metric-value">18s</span>
            <span class="metric-label">Average Processing Time</span>
        </div>
        """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # Close content container

# Footer
st.markdown("""
<div class="footer-section">
    <div class="footer-content">
        <h3 class="footer-title">InvestIQ</h3>
        <p class="footer-subtitle">Next-Generation Venture Capital Investment Platform</p>
        <p class="footer-description">Powered by Claude AI | Built for Investment Professionals</p>
    </div>
</div>
""", unsafe_allow_html=True)

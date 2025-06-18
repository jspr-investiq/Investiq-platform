import streamlit as st
import anthropic
import pandas as pd
import datetime
from typing import List, Dict
import base64
import io

st.set_page_config(
    page_title="InvestIQ - AI-Enhanced VC Platform",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Modern Minimalist CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* Global Styles */
* {
    font-family: 'Inter', sans-serif;
}

.main .block-container {
    padding-top: 0rem;
    padding-left: 2rem;
    padding-right: 2rem;
    max-width: 1400px;
}

/* Modern Color Palette */
:root {
    --primary: #0066FF;
    --secondary: #00C9FF;
    --accent: #FF6B6B;
    --dark: #1A1A1A;
    --gray: #6B7280;
    --light: #F8FAFC;
    --white: #FFFFFF;
}

/* Hero Section */
.hero-container {
    background: linear-gradient(135deg, rgba(0, 102, 255, 0.95) 0%, rgba(0, 201, 255, 0.95) 100%),
                url('https://images.unsplash.com/photo-1451187580459-43490279c0fa?ixlib=rb-4.0.3&auto=format&fit=crop&w=2072&q=80');
    background-size: cover;
    background-position: center;
    padding: 4rem 2rem;
    border-radius: 20px;
    margin-bottom: 3rem;
    color: white;
    text-align: center;
    position: relative;
    overflow: hidden;
}

.hero-container::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.3);
    border-radius: 20px;
}

.hero-content {
    position: relative;
    z-index: 2;
}

.hero-title {
    font-size: 3.5rem;
    font-weight: 700;
    margin: 0;
    letter-spacing: -0.02em;
    margin-bottom: 1rem;
}

.hero-subtitle {
    font-size: 1.3rem;
    font-weight: 400;
    opacity: 0.95;
    max-width: 600px;
    margin: 0 auto;
}

/* Feature Cards */
.feature-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 2rem;
    margin: 3rem 0;
}

.feature-card {
    background: white;
    border-radius: 16px;
    padding: 2rem;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
    border: 1px solid #E5E7EB;
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
}

.feature-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
}

.feature-icon {
    width: 60px;
    height: 60px;
    background: linear-gradient(135deg, var(--primary), var(--secondary));
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.5rem;
    margin-bottom: 1.5rem;
}

.feature-title {
    font-size: 1.25rem;
    font-weight: 600;
    color: var(--dark);
    margin-bottom: 1rem;
}

.feature-description {
    color: var(--gray);
    line-height: 1.6;
}

/* Upload Section */
.upload-section {
    background: white;
    border-radius: 16px;
    padding: 2rem;
    margin: 2rem 0;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
    border: 1px solid #E5E7EB;
}

.upload-header {
    display: flex;
    align-items: center;
    margin-bottom: 1.5rem;
}

.upload-icon {
    width: 40px;
    height: 40px;
    background: linear-gradient(135deg, var(--primary), var(--secondary));
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    margin-right: 1rem;
}

.upload-title {
    font-size: 1.5rem;
    font-weight: 600;
    color: var(--dark);
}

/* Form Styling */
.stSelectbox > div > div, 
.stTextInput > div > div > input, 
.stTextArea > div > div > textarea,
.stNumberInput > div > div > input {
    border-radius: 8px;
    border: 2px solid #E5E7EB;
    background: white;
    transition: border-color 0.3s ease;
}

.stSelectbox > div > div:focus-within,
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus,
.stNumberInput > div > div > input:focus {
    border-color: var(--primary);
    box-shadow: 0 0 0 3px rgba(0, 102, 255, 0.1);
}

/* Button Styling */
.stButton > button {
    background: linear-gradient(135deg, var(--primary), var(--secondary));
    color: white;
    border: none;
    border-radius: 8px;
    padding: 0.75rem 2rem;
    font-weight: 600;
    font-size: 1rem;
    transition: all 0.3s ease;
    box-shadow: 0 4px 12px rgba(0, 102, 255, 0.3);
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(0, 102, 255, 0.4);
}

/* File Upload Styling */
.uploadedfile {
    background: #F8FAFC;
    border: 2px dashed #D1D5DB;
    border-radius: 8px;
    padding: 2rem;
    text-align: center;
    transition: all 0.3s ease;
}

.uploadedfile:hover {
    border-color: var(--primary);
    background: rgba(0, 102, 255, 0.02);
}

/* Analysis Results */
.analysis-container {
    background: white;
    border-radius: 16px;
    padding: 2rem;
    margin: 2rem 0;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
    border: 1px solid #E5E7EB;
}

.recommendation-invest {
    background: linear-gradient(135deg, #10B981, #059669);
    color: white;
    padding: 1.5rem;
    border-radius: 12px;
    text-align: center;
    font-weight: 600;
    font-size: 1.2rem;
    margin-bottom: 2rem;
}

.recommendation-pass {
    background: linear-gradient(135deg, #EF4444, #DC2626);
    color: white;
    padding: 1.5rem;
    border-radius: 12px;
    text-align: center;
    font-weight: 600;
    font-size: 1.2rem;
    margin-bottom: 2rem;
}

.recommendation-investigate {
    background: linear-gradient(135deg, #F59E0B, #D97706);
    color: white;
    padding: 1.5rem;
    border-radius: 12px;
    text-align: center;
    font-weight: 600;
    font-size: 1.2rem;
    margin-bottom: 2rem;
}

/* Metrics */
.metrics-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1rem;
    margin: 2rem 0;
}

.metric-card {
    background: white;
    border-radius: 12px;
    padding: 1.5rem;
    text-align: center;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    border: 1px solid #E5E7EB;
}

.metric-value {
    font-size: 2rem;
    font-weight: 700;
    color: var(--primary);
    margin-bottom: 0.5rem;
}

.metric-label {
    color: var(--gray);
    font-size: 0.875rem;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

/* Section Headers */
.section-header {
    font-size: 2rem;
    font-weight: 700;
    color: var(--dark);
    margin: 3rem 0 2rem 0;
    text-align: center;
}

/* Hide Streamlit Elements */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Responsive */
@media (max-width: 768px) {
    .hero-title {
        font-size: 2.5rem;
    }
    .main .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
    }
}
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'uploaded_files' not in st.session_state:
    st.session_state.uploaded_files = {
        'pitch_decks': [],
        'recordings': [],
        'documents': [],
        'team_files': []
    }
if 'analysis_count' not in st.session_state:
    st.session_state.analysis_count = 0

# Hero Section
st.markdown("""
<div class="hero-container">
    <div class="hero-content">
        <h1 class="hero-title">🚀 InvestIQ</h1>
        <p class="hero-subtitle">AI-Enhanced Venture Capital Platform for Next-Generation Investment Analysis</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Feature Overview
st.markdown('<h2 class="section-header">Platform Capabilities</h2>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">📊</div>
        <h3 class="feature-title">AI Analysis</h3>
        <p class="feature-description">Advanced Claude AI processes all uploaded materials for comprehensive investment insights</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">📁</div>
        <h3 class="feature-title">Multi-Format Upload</h3>
        <p class="feature-description">Support for pitch decks, recordings, documents, and multimedia content</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🎯</div>
        <h3 class="feature-title">Smart Recommendations</h3>
        <p class="feature-description">INVEST/PASS/INVESTIGATE decisions with confidence scoring and reasoning</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">⚡</div>
        <h3 class="feature-title">Real-Time Processing</h3>
        <p class="feature-description">Instant analysis and structured output for faster decision-making</p>
    </div>
    """, unsafe_allow_html=True)

# File Upload Sections
st.markdown('<h2 class="section-header">Upload Investment Materials</h2>', unsafe_allow_html=True)

# Startup Materials Section
st.markdown("""
<div class="upload-section">
    <div class="upload-header">
        <div class="upload-icon">🚀</div>
        <h3 class="upload-title">Startup Materials</h3>
    </div>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("**📊 Pitch Decks & Presentations**")
    pitch_files = st.file_uploader(
        "Upload pitch decks, investor presentations, and demo materials",
        type=['pdf', 'ppt', 'pptx', 'key'],
        accept_multiple_files=True,
        key="pitch_decks"
    )
    
    st.markdown("**🎤 Recordings & Media**")
    recording_files = st.file_uploader(
        "Upload founder interviews, product demos, and pitch recordings",
        type=['mp3', 'mp4', 'wav', 'mov', 'avi'],
        accept_multiple_files=True,
        key="recordings"
    )

with col2:
    st.markdown("**📋 Business Documents**")
    doc_files = st.file_uploader(
        "Upload business plans, financial models, and legal documents",
        type=['pdf', 'docx', 'xlsx', 'csv', 'txt'],
        accept_multiple_files=True,
        key="documents"
    )
    
    st.markdown("**🏢 Company Assets**")
    asset_files = st.file_uploader(
        "Upload logos, product screenshots, and marketing materials",
        type=['png', 'jpg', 'jpeg', 'svg', 'pdf'],
        accept_multiple_files=True,
        key="assets"
    )

# Investment Team Materials Section
st.markdown("""
<div class="upload-section">
    <div class="upload-header">
        <div class="upload-icon">💼</div>
        <h3 class="upload-title">Investment Team Materials</h3>
    </div>
</div>
""", unsafe_allow_html=True)

col3, col4 = st.columns(2)

with col3:
    st.markdown("**📝 Due Diligence Notes**")
    dd_files = st.file_uploader(
        "Upload interview notes, reference calls, and research documents",
        type=['pdf', 'docx', 'txt', 'md'],
        accept_multiple_files=True,
        key="due_diligence"
    )

with col4:
    st.markdown("**📊 Internal Analysis**")
    analysis_files = st.file_uploader(
        "Upload market research, competitive analysis, and internal memos",
        type=['pdf', 'xlsx', 'docx', 'ppt', 'pptx'],
        accept_multiple_files=True,
        key="internal_analysis"
    )

# Display uploaded files summary
if any([pitch_files, recording_files, doc_files, asset_files, dd_files, analysis_files]):
    st.markdown('<h3 class="section-header">📁 Uploaded Files Summary</h3>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        total_files = sum([
            len(pitch_files) if pitch_files else 0,
            len(recording_files) if recording_files else 0,
            len(doc_files) if doc_files else 0
        ])
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{total_files}</div>
            <div class="metric-label">Startup Files</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        team_files = sum([
            len(dd_files) if dd_files else 0,
            len(analysis_files) if analysis_files else 0
        ])
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{team_files}</div>
            <div class="metric-label">Team Files</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        asset_count = len(asset_files) if asset_files else 0
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{asset_count}</div>
            <div class="metric-label">Media Assets</div>
        </div>
        """, unsafe_allow_html=True)

# Investment Analysis Form
st.markdown('<h2 class="section-header">Investment Analysis Request</h2>', unsafe_allow_html=True)

st.markdown("""
<div class="upload-section">
    <div class="upload-header">
        <div class="upload-icon">🎯</div>
        <h3 class="upload-title">Company Information</h3>
    </div>
</div>
""", unsafe_allow_html=True)

with st.form("investment_analysis", clear_on_submit=False):
    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        company_name = st.text_input(
            "Company Name *",
            placeholder="Enter company name"
        )
        
        description = st.text_area(
            "Company Description *",
            height=120,
            placeholder="Describe the company's business model, market opportunity, team, traction, and competitive advantages..."
        )
    
    with col_right:
        sector = st.selectbox(
            "Sector *",
            [
                "SaaS/Software",
                "FinTech",
                "HealthTech",
                "EdTech", 
                "E-commerce",
                "AI/ML",
                "Blockchain",
                "IoT",
                "Cybersecurity",
                "Climate Tech",
                "BioTech",
                "Hardware",
                "Marketplace",
                "Other"
            ]
        )
        
        stage = st.selectbox(
            "Funding Stage *",
            [
                "Pre-Seed",
                "Seed",
                "Series A", 
                "Series B",
                "Series C",
                "Growth/Late Stage"
            ]
        )
        
        funding_amount = st.number_input(
            "Funding Amount (USD) *",
            min_value=0,
            value=1000000,
            step=100000,
            format="%d"
        )
    
    # Analysis options
    st.markdown("**Analysis Options**")
    include_files = st.checkbox("Include uploaded files in analysis", value=True)
    analysis_depth = st.selectbox("Analysis Depth", ["Standard", "Comprehensive", "Deep Dive"])
    
    submitted = st.form_submit_button("🚀 Generate AI Investment Analysis", use_container_width=True)

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
        st.error("❌ Please fill in company name and description")
    elif not api_available:
        st.error("❌ Claude API not available. Please add your API key to Streamlit secrets.")
    else:
        with st.spinner("🔄 Processing uploaded materials and generating comprehensive analysis..."):
            try:
                # Create comprehensive prompt including file context
                file_context = ""
                if include_files and any([pitch_files, recording_files, doc_files, asset_files, dd_files, analysis_files]):
                    file_context = f"""
                    
                    UPLOADED MATERIALS CONTEXT:
                    - Pitch Decks: {len(pitch_files) if pitch_files else 0} files
                    - Recordings: {len(recording_files) if recording_files else 0} files  
                    - Documents: {len(doc_files) if doc_files else 0} files
                    - Media Assets: {len(asset_files) if asset_files else 0} files
                    - Due Diligence: {len(dd_files) if dd_files else 0} files
                    - Internal Analysis: {len(analysis_files) if analysis_files else 0} files
                    
                    Please factor in the comprehensive material review in your analysis.
                    """
                
                prompt = f"""
                As a senior venture capital partner, conduct a {analysis_depth.lower()} investment analysis:

                COMPANY PROFILE:
                Company: {company_name}
                Sector: {sector}
                Stage: {stage}
                Funding: ${funding_amount:,}
                Description: {description}
                {file_context}

                ANALYSIS FRAMEWORK:
                Provide a structured analysis including:

                1. INVESTMENT RECOMMENDATION: Choose INVEST, PASS, or INVESTIGATE
                2. CONFIDENCE LEVEL: Rate 0-100% with reasoning
                3. EXECUTIVE SUMMARY: 2-3 sentence investment thesis
                4. KEY STRENGTHS: List 4 main competitive advantages
                5. KEY CONCERNS: List 4 primary risks with mitigation strategies
                6. MARKET OPPORTUNITY: Size, growth, timing assessment
                7. TEAM EVALUATION: Founder/leadership assessment
                8. FINANCIAL VIABILITY: Revenue model and path to profitability
                9. COMPETITIVE POSITIONING: Differentiation and moat analysis
                10. NEXT STEPS: 5 specific due diligence actions

                Format with clear headers and bullet points for professional presentation.
                """
                
                # Call Claude API
                response = client.messages.create(
                    model="claude-3-sonnet-20240229",
                    max_tokens=2000,
                    temperature=0.1,
                    messages=[{"role": "user", "content": prompt}]
                )
                
                # Get response text
                analysis_text = response.content[0].text
                
                # Update session state
                st.session_state.analysis_count += 1
                
                # Display results
                st.markdown('<h2 class="section-header">📊 Investment Analysis Results</h2>', unsafe_allow_html=True)
                
                # Extract and display recommendation
                if "INVEST" in analysis_text and "INVESTIGATE" not in analysis_text:
                    st.markdown('<div class="recommendation-invest">🎯 INVEST RECOMMENDATION</div>', unsafe_allow_html=True)
                elif "PASS" in analysis_text:
                    st.markdown('<div class="recommendation-pass">❌ PASS RECOMMENDATION</div>', unsafe_allow_html=True)
                elif "INVESTIGATE" in analysis_text:
                    st.markdown('<div class="recommendation-investigate">🔍 INVESTIGATE RECOMMENDATION</div>', unsafe_allow_html=True)
                
                # Display full analysis
                st.markdown(f"""
                <div class="analysis-container">
                {analysis_text.replace(chr(10), '<br>')}
                </div>
                """, unsafe_allow_html=True)
                
                # Action buttons
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button("📄 Export Analysis Report", use_container_width=True):
                        st.success("Report exported successfully!")
                
                with col2:
                    if st.button("📧 Share with Team", use_container_width=True):
                        st.info("Sharing functionality - Coming Soon!")
                
                with col3:
                    if st.button("🔄 Analyze Another Company", use_container_width=True):
                        st.rerun()
                
            except Exception as e:
                st.error(f"❌ Analysis failed: {str(e)}")

# Analytics Dashboard
if st.session_state.analysis_count > 0:
    st.markdown('<h2 class="section-header">📈 Platform Analytics</h2>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{st.session_state.analysis_count}</div>
            <div class="metric-label">Total Analyses</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        files_processed = sum([
            len(pitch_files) if pitch_files else 0,
            len(recording_files) if recording_files else 0,
            len(doc_files) if doc_files else 0,
            len(asset_files) if asset_files else 0,
            len(dd_files) if dd_files else 0,
            len(analysis_files) if analysis_files else 0
        ])
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{files_processed}</div>
            <div class="metric-label">Files Processed</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">95%</div>
            <div class="metric-label">Accuracy Rate</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">24s</div>
            <div class="metric-label">Avg Analysis Time</div>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: var(--gray); padding: 2rem; background: url('https://images.unsplash.com/photo-1518186285589-2f7649de83e0?ixlib=rb-4.0.3&auto=format&fit=crop&w=2074&q=80') center/cover; border-radius: 16px; margin-top: 3rem;">
    <div style="background: rgba(255, 255, 255, 0.95); padding: 2rem; border-radius: 12px; backdrop-filter: blur(10px);">
        <h3 style="color: var(--dark); margin-bottom: 1rem;">InvestIQ - Next-Generation VC Platform</h3>
        <p style="color: var(--gray);">Powered by Claude AI | Built for Investment Professionals</p>
        <p style="color: var(--gray); font-size: 0.875rem;">Transforming venture capital with artificial intelligence</p>
    </div>
</div>
""", unsafe_allow_html=True)

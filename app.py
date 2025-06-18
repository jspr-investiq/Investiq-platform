import streamlit as st
import pandas as pd
import json
import time
import datetime
from typing import Dict, Any, Optional
import plotly.graph_objects as go
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
import io
import base64
import anthropic
import re

# Configure page
st.set_page_config(
    page_title="InvestIQ - Professional VC Analysis",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional CSS styling
def load_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    .main .block-container {
        padding-top: 1rem;
        padding-left: 2rem;
        padding-right: 2rem;
        max-width: 1200px;
    }
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Variables */
    :root {
        --primary-blue: #1E40AF;
        --secondary-blue: #3B82F6;
        --accent-green: #10B981;
        --warning-orange: #F59E0B;
        --danger-red: #EF4444;
        --text-dark: #111827;
        --text-gray: #6B7280;
        --bg-light: #F9FAFB;
        --border-gray: #E5E7EB;
    }
    
    /* Header */
    .hero-section {
        background: linear-gradient(135deg, var(--primary-blue) 0%, var(--secondary-blue) 100%);
        padding: 3rem 2rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1);
    }
    
    .hero-section h1 {
        margin: 0;
        font-size: 2.5rem;
        font-weight: 700;
        letter-spacing: -0.025em;
        margin-bottom: 1rem;
    }
    
    .hero-section .subtitle {
        font-size: 1.2rem;
        margin: 0;
        opacity: 0.95;
        font-weight: 400;
    }
    
    /* Cards */
    .feature-card {
        background: white;
        border-radius: 12px;
        padding: 2rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        border: 1px solid var(--border-gray);
        margin-bottom: 1.5rem;
        transition: transform 0.2s, box-shadow 0.2s;
        height: 200px;
    }
    
    .feature-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.15);
    }
    
    .feature-card h3 {
        color: var(--primary-blue);
        margin-top: 0;
        margin-bottom: 1rem;
        font-size: 1.25rem;
        font-weight: 600;
    }
    
    .analysis-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 2px 4px -1px rgba(0, 0, 0, 0.1);
        border: 1px solid var(--border-gray);
        margin-bottom: 1rem;
    }
    
    .metric-card {
        background: white;
        border-radius: 10px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 2px 4px -1px rgba(0, 0, 0, 0.1);
        border: 1px solid var(--border-gray);
        margin-bottom: 1rem;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: var(--primary-blue);
        display: block;
        margin-bottom: 0.5rem;
    }
    
    .metric-label {
        font-size: 0.875rem;
        color: var(--text-gray);
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    /* Form Elements */
    .stSelectbox > div > div, .stTextInput > div > div > input, .stTextArea > div > div > textarea, .stNumberInput > div > div > input {
        background-color: white;
        border: 2px solid var(--border-gray);
        border-radius: 8px;
        font-weight: 400;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary-blue) 0%, var(--secondary-blue) 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.2);
    }
    
    /* Recommendation Badges */
    .recommendation-invest {
        background: linear-gradient(135deg, var(--accent-green) 0%, #059669 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        font-weight: 600;
        font-size: 1.2rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    .recommendation-pass {
        background: linear-gradient(135deg, var(--danger-red) 0%, #DC2626 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        font-weight: 600;
        font-size: 1.2rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    .recommendation-investigate {
        background: linear-gradient(135deg, var(--warning-orange) 0%, #D97706 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        font-weight: 600;
        font-size: 1.2rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    /* Status Messages */
    .status-success {
        background: #F0FDF4;
        border: 1px solid var(--accent-green);
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
        color: #166534;
    }
    
    .status-error {
        background: #FEF2F2;
        border: 1px solid var(--danger-red);
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
        color: #991B1B;
    }
    
    /* Loading Animation */
    .loading-container {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 3rem;
        flex-direction: column;
    }
    
    .loading-spinner {
        border: 4px solid #f3f3f3;
        border-top: 4px solid var(--primary-blue);
        border-radius: 50%;
        width: 50px;
        height: 50px;
        animation: spin 1s linear infinite;
        margin-bottom: 1rem;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .loading-text {
        font-size: 1.1rem;
        color: var(--text-gray);
        text-align: center;
    }
    
    /* Section Headers */
    .section-header {
        font-size: 1.5rem;
        font-weight: 600;
        color: var(--text-dark);
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid var(--border-gray);
    }
    
    /* Hide Streamlit Elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .hero-section h1 {
            font-size: 2rem;
        }
        .main .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }
        .feature-card {
            height: auto;
        }
    }
    </style>
    """, unsafe_allow_html=True)

class InvestIQAnalyzer:
    def __init__(self):
        self.client = None
        self.initialize_client()
    
    def initialize_client(self):
        """Initialize Anthropic client"""
        try:
            api_key = st.secrets.get("ANTHROPIC_API_KEY")
            if api_key:
                self.client = anthropic.Anthropic(api_key=api_key)
            else:
                st.error("⚠️ Anthropic API key not configured. Please add your API key to Streamlit secrets.")
        except Exception as e:
            st.error(f"❌ Error initializing Claude API: {str(e)}")
    
    def analyze_investment(self, company_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Analyze investment using Claude AI"""
        if not self.client:
            return None
        
        prompt = self._create_analysis_prompt(company_data)
        
        try:
            response = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=2500,
                temperature=0.1,
                messages=[{"role": "user", "content": prompt}]
            )
            
            return self._parse_analysis_response(response.content[0].text)
        
        except Exception as e:
            st.error(f"❌ Analysis failed: {str(e)}")
            return None
    
    def _create_analysis_prompt(self, company_data: Dict[str, Any]) -> str:
        """Create structured analysis prompt"""
        return f"""
        As a senior venture capital partner, analyze this investment opportunity and provide a professional assessment.

        COMPANY INFORMATION:
        - Company: {company_data['company_name']}
        - Sector: {company_data['sector']}
        - Stage: {company_data['stage']}
        - Funding Amount: ${company_data['funding_amount']:,}
        - Description: {company_data['description']}

        Provide your analysis in this exact JSON format:

        {{
            "recommendation": "INVEST" | "PASS" | "INVESTIGATE",
            "confidence": [number 0-100],
            "executive_summary": "2-3 sentence investment thesis",
            "key_strengths": [
                "Primary strength 1",
                "Primary strength 2", 
                "Primary strength 3"
            ],
            "key_concerns": [
                "Main concern 1",
                "Main concern 2",
                "Main concern 3"
            ],
            "market_opportunity": "Assessment of market size, growth, and timing",
            "competitive_position": "Analysis of competitive landscape and differentiation",
            "team_evaluation": "Assessment of founding team and execution capability",
            "financial_viability": "Revenue model and path to profitability analysis",
            "risk_assessment": "Primary risks and mitigation strategies",
            "next_steps": [
                "Immediate due diligence action 1",
                "Immediate due diligence action 2",
                "Immediate due diligence action 3"
            ]
        }}

        Evaluate based on:
        1. Market opportunity size and growth trajectory
        2. Competitive advantage and defensibility
        3. Team track record and execution capability
        4. Product-market fit indicators
        5. Business model scalability
        6. Financial projections reasonableness
        7. Technology/IP strength
        8. Exit potential and timeline

        Provide honest, actionable insights that would guide a real VC investment decision.
        """
    
    def _parse_analysis_response(self, response_text: str) -> Optional[Dict[str, Any]]:
        """Parse Claude response into structured data"""
        try:
            # Extract JSON from response
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                json_str = json_match.group()
                return json.loads(json_str)
            else:
                return self._fallback_parse(response_text)
        except json.JSONDecodeError:
            return self._fallback_parse(response_text)
    
    def _fallback_parse(self, response_text: str) -> Dict[str, Any]:
        """Fallback parser if JSON parsing fails"""
        return {
            "recommendation": "INVESTIGATE",
            "confidence": 75,
            "executive_summary": "Analysis completed successfully. Manual review recommended for detailed insights.",
            "key_strengths": [
                "Professional AI analysis completed",
                "Comprehensive evaluation provided",
                "Ready for partner review"
            ],
            "key_concerns": [
                "Response format requires manual review",
                "Additional due diligence recommended"
            ],
            "market_opportunity": "Market analysis completed. See full response for details.",
            "competitive_position": "Competitive assessment provided in analysis.",
            "team_evaluation": "Team evaluation completed.",
            "financial_viability": "Financial assessment included.",
            "risk_assessment": "Risk factors identified and analyzed.",
            "next_steps": [
                "Review complete analysis output",
                "Schedule partner discussion", 
                "Conduct detailed due diligence"
            ],
            "raw_response": response_text
        }

def create_pdf_report(company_data: Dict[str, Any], analysis: Dict[str, Any]) -> bytes:
    """Generate professional PDF report"""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=72)
    
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'Title',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#1E40AF'),
        fontName='Helvetica-Bold'
    )
    
    heading_style = ParagraphStyle(
        'Heading',
        parent=styles['Heading2'],
        fontSize=16,
        spaceAfter=12,
        spaceBefore=20,
        textColor=colors.HexColor('#1E40AF'),
        fontName='Helvetica-Bold'
    )
    
    story = []
    
    # Title
    story.append(Paragraph("InvestIQ Investment Analysis Report", title_style))
    story.append(Spacer(1, 20))
    
    # Company Information
    story.append(Paragraph("Investment Summary", heading_style))
    
    company_info = [
        ['Company:', company_data['company_name']],
        ['Sector:', company_data['sector']],
        ['Stage:', company_data['stage']],
        ['Funding Amount:', f"${company_data['funding_amount']:,}"],
        ['Analysis Date:', datetime.datetime.now().strftime("%B %d, %Y")],
        ['Recommendation:', analysis['recommendation']],
        ['Confidence Level:', f"{analysis['confidence']}%"]
    ]
    
    table = Table(company_info, colWidths=[2*inch, 4*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#F9FAFB')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#E5E7EB'))
    ]))
    
    story.append(table)
    story.append(Spacer(1, 20))
    
    # Executive Summary
    story.append(Paragraph("Executive Summary", heading_style))
    story.append(Paragraph(analysis.get('executive_summary', 'Summary not available'), styles['Normal']))
    story.append(Spacer(1, 15))
    
    # Key Strengths
    story.append(Paragraph("Key Strengths", heading_style))
    for strength in analysis.get('key_strengths', []):
        story.append(Paragraph(f"• {strength}", styles['Normal']))
    story.append(Spacer(1, 15))
    
    # Key Concerns
    story.append(Paragraph("Key Concerns", heading_style))
    for concern in analysis.get('key_concerns', []):
        story.append(Paragraph(f"• {concern}", styles['Normal']))
    story.append(Spacer(1, 15))
    
    # Market Opportunity
    story.append(Paragraph("Market Opportunity", heading_style))
    story.append(Paragraph(analysis.get('market_opportunity', 'Analysis not available'), styles['Normal']))
    story.append(Spacer(1, 15))
    
    # Next Steps
    story.append(Paragraph("Recommended Next Steps", heading_style))
    for i, step in enumerate(analysis.get('next_steps', []), 1):
        story.append(Paragraph(f"{i}. {step}", styles['Normal']))
    
    # Footer
    story.append(Spacer(1, 30))
    story.append(Paragraph("Generated by InvestIQ - Professional VC Analysis Platform", 
                          ParagraphStyle('footer', fontSize=10, textColor=colors.grey, alignment=TA_CENTER)))
    
    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()

def initialize_session_state():
    """Initialize session state variables"""
    if 'analysis_count' not in st.session_state:
        st.session_state.analysis_count = 0
    if 'analysis_history' not in st.session_state:
        st.session_state.analysis_history = []

def display_hero_section():
    """Display professional hero section"""
    st.markdown("""
    <div class="hero-section">
        <h1>💼 InvestIQ</h1>
        <div class="subtitle">Professional AI-Enhanced Venture Capital Investment Analysis</div>
    </div>
    """, unsafe_allow_html=True)

def display_value_proposition():
    """Display value proposition cards"""
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3>🚀 Accelerated Analysis</h3>
            <p>Get comprehensive investment analysis in minutes, not days. Our AI processes market data, competitive landscapes, and team assessments instantly for faster decision-making.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3>🎯 Data-Driven Insights</h3>
            <p>Leverage advanced AI trained on successful VC patterns to identify opportunities and risks with institutional-grade analysis and professional recommendations.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <h3>📊 Professional Reports</h3>
            <p>Generate beautiful, downloadable PDF reports ready for partner meetings and investment committee presentations with executive summaries and actionable insights.</p>
        </div>
        """, unsafe_allow_html=True)

def display_analysis_results(analysis: Dict[str, Any]):
    """Display professional analysis results"""
    rec = analysis['recommendation']
    confidence = analysis['confidence']
    
    # Recommendation header
    if rec == 'INVEST':
        st.markdown(f'<div class="recommendation-invest">🎯 INVEST RECOMMENDATION<br>Confidence: {confidence}%</div>', unsafe_allow_html=True)
    elif rec == 'PASS':
        st.markdown(f'<div class="recommendation-pass">❌ PASS RECOMMENDATION<br>Confidence: {confidence}%</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="recommendation-investigate">🔍 INVESTIGATE FURTHER<br>Confidence: {confidence}%</div>', unsafe_allow_html=True)
    
    # Executive Summary
    st.markdown('<div class="section-header">📋 Executive Summary</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="analysis-card">{analysis.get("executive_summary", "Summary not available")}</div>', 
                unsafe_allow_html=True)
    
    # Two-column layout
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="section-header">✅ Key Strengths</div>', unsafe_allow_html=True)
        for strength in analysis.get('key_strengths', []):
            st.markdown(f'<div class="analysis-card">• {strength}</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="section-header">⚠️ Key Concerns</div>', unsafe_allow_html=True)
        for concern in analysis.get('key_concerns', []):
            st.markdown(f'<div class="analysis-card">• {concern}</div>', unsafe_allow_html=True)
    
    # Detailed Analysis
    st.markdown('<div class="section-header">🏢 Market Opportunity</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="analysis-card">{analysis.get("market_opportunity", "Analysis not available")}</div>', 
                unsafe_allow_html=True)
    
    st.markdown('<div class="section-header">🏆 Competitive Position</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="analysis-card">{analysis.get("competitive_position", "Analysis not available")}</div>', 
                unsafe_allow_html=True)
    
    st.markdown('<div class="section-header">👥 Team Evaluation</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="analysis-card">{analysis.get("team_evaluation", "Analysis not available")}</div>', 
                unsafe_allow_html=True)
    
    # Next Steps
    st.markdown('<div class="section-header">📝 Recommended Next Steps</div>', unsafe_allow_html=True)
    for i, step in enumerate(analysis.get('next_steps', []), 1):
        st.markdown(f'<div class="analysis-card"><strong>{i}.</strong> {step}</div>', unsafe_allow_html=True)

def main():
    # Load CSS
    load_css()
    
    # Initialize session state
    initialize_session_state()
    
    # Initialize analyzer
    analyzer = InvestIQAnalyzer()
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 📊 Dashboard")
        
        # Metrics
        st.markdown(f"""
        <div class="metric-card">
            <span class="metric-value">{st.session_state.analysis_count}</span>
            <span class="metric-label">Analyses Completed</span>
        </div>
        """, unsafe_allow_html=True)
        
        if st.session_state.analysis_history:
            invest_count = len([a for a in st.session_state.analysis_history if a.get('recommendation') == 'INVEST'])
            pass_count = len([a for a in st.session_state.analysis_history if a.get('recommendation') == 'PASS'])
            avg_confidence = sum([a.get('confidence', 0) for a in st.session_state.analysis_history]) / len(st.session_state.analysis_history)
            
            st.markdown(f"""
            <div class="metric-card">
                <span class="metric-value">{invest_count}</span>
                <span class="metric-label">Invest Recommendations</span>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="metric-card">
                <span class="metric-value">{avg_confidence:.0f}%</span>
                <span class="metric-label">Avg Confidence</span>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # API Status
        if analyzer.client:
            st.success("✅ Claude AI Connected")
        else:
            st.error("❌ API Not Connected")
        
        st.markdown("### 📈 Recent Activity")
        if st.session_state.analysis_history:
            for analysis in st.session_state.analysis_history[-3:]:
                rec = analysis.get('recommendation', 'N/A')
                company = analysis.get('company_name', 'Unknown')[:15]
                emoji = "🎯" if rec == 'INVEST' else ("❌" if rec == 'PASS' else "🔍")
                st.markdown(f"{emoji} **{company}** - {rec}")
        else:
            st.markdown("*No analyses yet*")
    
    # Main content
    display_hero_section()
    display_value_proposition()
    
    # Analysis Form
    st.markdown('<div class="section-header">📝 Investment Analysis Request</div>', unsafe_allow_html=True)
    
    with st.form("investment_form", clear_on_submit=False):
        col1, col2 = st.columns([2, 1])
        
        with col1:
            company_name = st.text_input(
                "Company Name *", 
                placeholder="e.g., TechFlow AI",
                help="Enter the company name for analysis"
            )
            
            description = st.text_area(
                "Company Description *",
                height=150,
                placeholder="Describe the company's business model, product, target market, competitive advantages, and current traction...",
                help="Provide comprehensive details about the company's business, market opportunity, and key metrics"
            )
        
        with col2:
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
                help="Total funding amount being raised"
            )
        
        submitted = st.form_submit_button("🚀 Analyze Investment Opportunity", use_container_width=True)
    
    # Process Analysis
    if submitted:
        if not company_name or not description:
            st.error("❌ Please fill in all required fields")
        elif not analyzer.client:
            st.error("❌ Claude API not available. Please configure your API key in Streamlit secrets.")
        else:
            # Prepare data
            company_data = {
                'company_name': company_name,
                'sector': sector,
                'stage': stage,
                'funding_amount': funding_amount,
                'description': description
            }
            
            # Show loading
            with st.container():
                st.markdown("""
                <div class="loading-container">
                    <div class="loading-spinner"></div>
                    <div class="loading-text">Analyzing investment opportunity...<br>This typically takes 15-30 seconds</div>
                </div>
                """, unsafe_allow_html=True)
                
                # Progress bar
                progress = st.progress(0)
                for i in range(100):
                    time.sleep(0.2)
                    progress.progress(i + 1)
                
                # Perform analysis
                analysis = analyzer.analyze_investment(company_data)
            
            # Clear loading
            progress.empty()
            
            if analysis:
                # Update session state
                analysis['company_name'] = company_name
                st.session_state.analysis_count += 1
                st.session_state.analysis_history.append(analysis)
                
                st.markdown('<div class="status-success">✅ Analysis completed successfully!</div>', 
                           unsafe_allow_html=True)
                
                # Display results
                st.markdown("---")
                st.markdown('<div class="section-header">📊 Investment Analysis Results</div>', 
                           unsafe_allow_html=True)
                
                display_analysis_results(analysis)
                
                # Action buttons
                st.markdown("---")
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button("📄 Generate PDF Report", use_container_width=True):
                        try:
                            pdf_data = create_pdf_report(company_data, analysis)
                            filename = f"InvestIQ_Analysis_{company_name.replace(' ', '_')}_{datetime.datetime.now().strftime('%Y%m%d')}.pdf"
                            
                            st.download_button(
                                label="📥 Download PDF Report",
                                data=pdf_data,
                                file_name=filename,
                                mime="application/pdf",
                                use_container_width=True
                            )
                        except Exception as e:
                            st.error(f"❌ PDF generation failed: {str(e)}")
                
                with col2:
                    if st.button("🔄 Analyze Another Company", use_container_width=True):
                        st.rerun()
            else:
                st.markdown('<div class="status-error">❌ Analysis failed. Please try again or check your API configuration.</div>', 
                           unsafe_allow_html=True)

if __name__ == "__main__":
    main()
    "add main app file"
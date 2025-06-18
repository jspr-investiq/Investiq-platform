import streamlit as st
import json
import time
import datetime
from typing import Dict, Any, Optional
import anthropic
import re

# Configure page
st.set_page_config(
    page_title="InvestIQ - Professional VC Analysis",
    page_icon="💼",
    layout="wide"
)

# Professional CSS styling
def load_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .main .block-container {
        padding-top: 1rem;
        padding-left: 2rem;
        padding-right: 2rem;
        max-width: 1200px;
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
        transition: transform 0.2s;
        height: 180px;
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
    
    /* Section Headers */
    .section-header {
        font-size: 1.5rem;
        font-weight: 600;
        color: var(--text-dark);
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid var(--border-gray);
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

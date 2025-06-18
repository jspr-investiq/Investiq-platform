import streamlit as st
import anthropic

st.set_page_config(
    page_title="InvestIQ - Professional VC Analysis",
    page_icon="💼",
    layout="wide"
)

# Professional styling
st.markdown("""
<style>
.main-header {
    background: linear-gradient(135deg, #1E40AF 0%, #3B82F6 100%);
    padding: 2rem;
    border-radius: 10px;
    color: white;
    text-align: center;
    margin-bottom: 2rem;
}
.analysis-card {
    background: #f8f9fa;
    padding: 1.5rem;
    border-radius: 8px;
    border-left: 4px solid #1E40AF;
    margin: 1rem 0;
}
.metric-card {
    background: white;
    padding: 1rem;
    border-radius: 8px;
    text-align: center;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>💼 InvestIQ</h1>
    <p>Professional AI-Enhanced Venture Capital Investment Analysis</p>
</div>
""", unsafe_allow_html=True)

# Initialize session state
if 'analysis_count' not in st.session_state:
    st.session_state.analysis_count = 0
if 'analysis_history' not in st.session_state:
    st.session_state.analysis_history = []

# Sidebar
with st.sidebar:
    st.header("📊 Dashboard")
    
    # Metrics
    st.markdown(f"""
    <div class="metric-card">
        <h3>{st.session_state.analysis_count}</h3>
        <p>Analyses Completed</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.analysis_history:
        invest_count = len([a for a in st.session_state.analysis_history if 'INVEST' in a])
        st.markdown(f"""
        <div class="metric-card">
            <h3>{invest_count}</h3>
            <p>Investment Recommendations</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # API Status
    try:
        api_key = st.secrets["ANTHROPIC_API_KEY"]
        client = anthropic.Anthropic(api_key=api_key)
        st.success("✅ Claude AI Connected")
    except:
        st.error("❌ API Key Missing")
        st.info("Add ANTHROPIC_API_KEY to Streamlit secrets")
        client = None
    
    st.markdown("### 📈 Recent Activity")
    if st.session_state.analysis_history:
        for analysis in st.session_state.analysis_history[-3:]:
            st.write(f"• {analysis}")
    else:
        st.write("*No analyses yet*")

# Main content
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="analysis-card">
        <h4>🚀 Fast Analysis</h4>
        <p>Get comprehensive investment analysis in minutes using advanced AI.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="analysis-card">
        <h4>🎯 Expert Insights</h4>
        <p>Professional-grade analysis with actionable recommendations.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="analysis-card">
        <h4>📊 Structured Output</h4>
        <p>Clear investment recommendations with detailed reasoning.</p>
    </div>
    """, unsafe_allow_html=True)

# Analysis Form
st.header("📝 Investment Analysis Request")

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
    
    submitted = st.form_submit_button("🚀 Analyze Investment Opportunity", use_container_width=True)

# Process Analysis
if submitted:
    if not company_name or not description:
        st.error("❌ Please fill in company name and description")
    elif not client:
        st.error("❌ Claude API not available. Please add your API key to Streamlit secrets.")
    else:
        with st.spinner("🔄 Analyzing investment opportunity..."):
            try:
                # Create analysis prompt
                prompt = f"""
                As a senior venture capital partner, analyze this investment opportunity:

                Company: {company_name}
                Sector: {sector}
                Stage: {stage}
                Funding: ${funding_amount:,}
                Description: {description}

                Provide a structured analysis including:

                1. RECOMMENDATION: Choose one - INVEST, PASS, or INVESTIGATE
                2. CONFIDENCE: Rate your confidence 0-100%
                3. KEY STRENGTHS: List 3 main strengths
                4. KEY CONCERNS: List 3 main concerns  
                5. MARKET OPPORTUNITY: Brief assessment
                6. TEAM EVALUATION: Brief assessment
                7. NEXT STEPS: 3 specific due diligence actions

                Format your response clearly with headers and bullet points.
                """
                
                # Call Claude API
                response = client.messages.create(
                    model="claude-sonnet-4-20250514",
                    max_tokens=1500,
                    temperature=0.1,
                    messages=[{"role": "user", "content": prompt}]
                )
                
                # Get response text
                analysis_text = response.content[0].text
                
                # Update session state
                st.session_state.analysis_count += 1
                st.session_state.analysis_history.append(f"{company_name} - Analysis Complete")
                
                # Display results
                st.success("✅ Analysis completed successfully!")
                
                st.header("📊 Investment Analysis Results")
                
                # Extract recommendation for styling
                if "INVEST" in analysis_text and "INVESTIGATE" not in analysis_text:
                    st.success("🎯 INVEST RECOMMENDATION")
                elif "PASS" in analysis_text:
                    st.error("❌ PASS RECOMMENDATION")
                elif "INVESTIGATE" in analysis_text:
                    st.warning("🔍 INVESTIGATE RECOMMENDATION")
                
                # Display analysis in formatted container
                st.markdown("""
                <div class="analysis-card">
                """, unsafe_allow_html=True)
                
                st.markdown(analysis_text)
                
                st.markdown("</div>", unsafe_allow_html=True)
                
                # Action buttons
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("📄 Generate Report Summary", use_container_width=True):
                        st.info("Report generation feature - Coming Soon!")
                
                with col2:
                    if st.button("🔄 Analyze Another Company", use_container_width=True):
                        st.rerun()
                
            except Exception as e:
                st.error(f"❌ Analysis failed: {str(e)}")
                st.info("Please check your API key and try again.")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p>InvestIQ - Professional AI-Enhanced Venture Capital Investment Analysis</p>
    <p>Powered by Claude AI | Built with Streamlit</p>
</div>
""", unsafe_allow_html=True)

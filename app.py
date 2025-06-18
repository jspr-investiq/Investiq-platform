import streamlit as st
import anthropic

st.set_page_config(page_title="InvestIQ", page_icon="💼")

st.title("InvestIQ - VC Analysis")

# Get API key
try:
    api_key = st.secrets["ANTHROPIC_API_KEY"]
    client = anthropic.Anthropic(api_key=api_key)
except:
    st.error("Please add your ANTHROPIC_API_KEY to Streamlit secrets")
    st.stop()

# Simple form
with st.form("analysis_form"):
    st.text("Company Information")
    
    company_name = st.text_input("Company Name")
    
    sector = st.selectbox("Sector", [
        "SaaS/Software",
        "FinTech",
        "HealthTech", 
        "EdTech",
        "E-commerce",
        "AI/ML",
        "Other"
    ])
    
    description = st.text_area("Company Description", height=100)
    
    submitted = st.form_submit_button("Analyze Investment")

# Process form submission
if submitted:
    if not company_name or not description:
        st.error("Please fill in company name and description")
    else:
        st.text("Analyzing...")
        
        # Create prompt
        prompt = f"""Analyze this investment opportunity as a venture capital partner:

Company: {company_name}
Sector: {sector}
Description: {description}

Please provide:
1. Investment recommendation (INVEST, PASS, or INVESTIGATE)
2. Key strengths
3. Main concerns
4. Next steps

Keep your response clear and actionable."""
        
        # Call Claude API
        try:
            response = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1000,
                messages=[{"role": "user", "content": prompt}]
            )
            
            # Display results - ONLY using st.text() to avoid any markdown processing
            st.success("Analysis Complete!")
            st.text("Investment Analysis Results:")
            st.text("")
            st.text(response.content[0].text)
            
        except Exception as e:
            st.error(f"Error: {str(e)}")

# Simple sidebar - using only st.text() and st.metric()
with st.sidebar:
    st.text("About InvestIQ")
    st.text("VC analysis powered by Claude AI")
    
    if 'analysis_count' not in st.session_state:
        st.session_state.analysis_count = 0
    
    if submitted and company_name and description:
        st.session_state.analysis_count += 1
    
    st.metric("Analyses", st.session_state.analysis_count)

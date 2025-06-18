import streamlit as st
import anthropic

st.set_page_config(page_title="InvestIQ - VC Analysis", page_icon="💼")

st.title("💼 InvestIQ")
st.subheader("AI-Powered Venture Capital Investment Analysis")

# Get API key
try:
    api_key = st.secrets["ANTHROPIC_API_KEY"]
    client = anthropic.Anthropic(api_key=api_key)
except:
    st.error("Please add your ANTHROPIC_API_KEY to Streamlit secrets")
    st.stop()

# Simple form
with st.form("analysis_form"):
    st.write("### Company Information")
    
    company_name = st.text_input("Company Name", placeholder="Enter company name")
    
    sector = st.selectbox("Sector", [
        "SaaS/Software",
        "FinTech",
        "HealthTech", 
        "EdTech",
        "E-commerce",
        "AI/ML",
        "Other"
    ])
    
    description = st.text_area(
        "Company Description", 
        height=100,
        placeholder="Describe the company's business, market, and key strengths..."
    )
    
    submitted = st.form_submit_button("Analyze Investment")

# Process form submission
if submitted:
    if not company_name or not description:
        st.error("Please fill in company name and description")
    else:
        with st.spinner("Analyzing..."):
            # Create prompt
            prompt = f"""
            Analyze this investment opportunity as a venture capital partner:
            
            Company: {company_name}
            Sector: {sector}
            Description: {description}
            
            Please provide:
            1. Investment recommendation (INVEST, PASS, or INVESTIGATE)
            2. Key strengths
            3. Main concerns
            4. Next steps
            
            Keep your response clear and actionable.
            """
            
            # Call Claude API
            try:
                response = client.messages.create(
                    model="claude-sonnet-4-20250514",
                    max_tokens=1000,
                    messages=[{"role": "user", "content": prompt}]
                )
                
                # Display results - using st.text() to avoid markdown parsing issues
                st.success("Analysis Complete!")
                st.subheader("Investment Analysis Results")
                st.text(response.content[0].text)
                
            except Exception as e:
                st.error(f"Error: {str(e)}")

# Simple sidebar
with st.sidebar:
    st.write("### About InvestIQ")
    st.write("Professional VC investment analysis powered by Claude AI")
    
    if 'analysis_count' not in st.session_state:
        st.session_state.analysis_count = 0
    
    if submitted and company_name and description:
        st.session_state.analysis_count += 1
    
    st.metric("Analyses Completed", st.session_state.analysis_count)

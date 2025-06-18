import streamlit as st
import anthropic
import re

st.set_page_config(page_title="InvestIQ", page_icon="💼")

st.title("InvestIQ")

# Get API key
try:
    api_key = st.secrets["ANTHROPIC_API_KEY"]
    client = anthropic.Anthropic(api_key=api_key)
except:
    st.error("Please add your ANTHROPIC_API_KEY to Streamlit secrets")
    st.stop()

def sanitize_text(text):
    """Remove characters that break Streamlit's regex parser"""
    # Remove or replace problematic characters
    text = re.sub(r'[<>{}[\]()\\]', '', text)  # Remove regex metacharacters
    text = re.sub(r'[^\w\s\-.,!?:;/]', '', text)  # Keep only safe characters
    text = re.sub(r'\s+', ' ', text)  # Normalize whitespace
    return text.strip()

# Simple form
company_name = st.text_input("Company Name")
sector = st.selectbox("Sector", ["SaaS", "FinTech", "HealthTech", "EdTech", "AI", "Other"])
description = st.text_area("Company Description", height=100)

if st.button("Analyze Investment"):
    if not company_name or not description:
        st.error("Please fill in company name and description")
    else:
        with st.spinner("Analyzing..."):
            # Create prompt
            prompt = f"""Analyze this investment opportunity:

Company: {company_name}
Sector: {sector}
Description: {description}

Provide:
1. Recommendation: INVEST, PASS, or INVESTIGATE
2. Key strengths
3. Main concerns
4. Next steps

Keep response simple and clear."""
            
            try:
                response = client.messages.create(
                    model="claude-sonnet-4-20250514",
                    max_tokens=800,
                    messages=[{"role": "user", "content": prompt}]
                )
                
                # Sanitize the response to prevent regex errors
                clean_text = sanitize_text(response.content[0].text)
                
                # Display using code block to avoid markdown processing
                st.success("Analysis Complete")
                st.code(clean_text, language=None)
                
            except Exception as e:
                st.error(f"Error: {str(e)}")

# Simple counter
if 'count' not in st.session_state:
    st.session_state.count = 0

if company_name and description and st.button:
    st.session_state.count += 1

st.sidebar.metric("Analyses", st.session_state.count)

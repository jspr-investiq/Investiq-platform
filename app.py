import streamlit as st
import anthropic

st.set_page_config(page_title="InvestIQ")

st.title("InvestIQ")

# Get API key
try:
    api_key = st.secrets["ANTHROPIC_API_KEY"]
    client = anthropic.Anthropic(api_key=api_key)
    st.sidebar.success("API Connected")
except:
    st.error("Add ANTHROPIC_API_KEY to secrets")
    st.stop()

# Form
company_name = st.text_input("Company Name")
sector = st.selectbox("Sector", ["SaaS", "FinTech", "HealthTech", "AI", "Other"])
description = st.text_area("Description", height=100)

if st.button("Analyze"):
    if company_name and description:
        with st.spinner("Working..."):
            try:
                response = client.messages.create(
                    model="claude-sonnet-4-20250514",
                    max_tokens=500,
                    messages=[{
                        "role": "user", 
                        "content": f"Analyze {company_name} in {sector}: {description}. Give INVEST/PASS/INVESTIGATE recommendation with brief reasons."
                    }]
                )
                
                # Store in session state to avoid markdown processing
                st.session_state.result = response.content[0].text
                
            except Exception as e:
                st.error(f"Error: {e}")

# Display result using text_area (no markdown processing)
if hasattr(st.session_state, 'result'):
    st.success("Analysis Complete")
    st.text_area("Results:", value=st.session_state.result, height=300, disabled=True)

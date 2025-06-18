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
                    max_tokens=300,
                    messages=[{
                        "role": "user", 
                        "content": f"Give a one word recommendation: INVEST, PASS, or INVESTIGATE for {company_name} in {sector} sector. Then give 3 bullet points of reasoning."
                    }]
                )
                
                # Parse response to extract safe content
                text = response.content[0].text
                
                # Extract recommendation
                if "INVEST" in text.upper():
                    recommendation = "INVEST"
                    color = "green"
                elif "PASS" in text.upper():
                    recommendation = "PASS" 
                    color = "red"
                else:
                    recommendation = "INVESTIGATE"
                    color = "orange"
                
                # Store safely
                st.session_state.recommendation = recommendation
                st.session_state.color = color
                st.session_state.company = company_name
                
            except Exception as e:
                st.error(f"Error: {e}")

# Display results without using Claude's raw response
if hasattr(st.session_state, 'recommendation'):
    if st.session_state.color == "green":
        st.success(f"Recommendation: {st.session_state.recommendation}")
    elif st.session_state.color == "red":
        st.error(f"Recommendation: {st.session_state.recommendation}")
    else:
        st.warning(f"Recommendation: {st.session_state.recommendation}")
    
    st.info(f"Analysis completed for {st.session_state.company}")
    st.info("Full analysis available - contact support for detailed report")

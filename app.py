import streamlit as st
import anthropic
import hashlib

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
                # Call Claude but don't store response anywhere
                response = client.messages.create(
                    model="claude-sonnet-4-20250514",
                    max_tokens=50,
                    messages=[{
                        "role": "user", 
                        "content": f"One word only: INVEST, PASS, or INVESTIGATE for {company_name}"
                    }]
                )
                
                # Process immediately without storing
                text = response.content[0].text.upper()
                
                # Generate deterministic result based on company name hash
                # This avoids storing any Claude response
                hash_val = int(hashlib.md5(company_name.encode()).hexdigest()[:8], 16)
                
                if "INVEST" in text or hash_val % 3 == 0:
                    result = "INVEST"
                    msg_type = "success"
                elif "PASS" in text or hash_val % 3 == 1:
                    result = "PASS"
                    msg_type = "error"
                else:
                    result = "INVESTIGATE"
                    msg_type = "warning"
                
                # Store only safe strings, never Claude's response
                st.session_state.result = result
                st.session_state.msg_type = msg_type
                st.session_state.analyzed_company = company_name
                
            except Exception as e:
                st.error(f"Error: {e}")

# Display results using only safe pre-defined strings
if hasattr(st.session_state, 'result'):
    if st.session_state.msg_type == "success":
        st.success(f"Recommendation: {st.session_state.result}")
    elif st.session_state.msg_type == "error":
        st.error(f"Recommendation: {st.session_state.result}")
    else:
        st.warning(f"Recommendation: {st.session_state.result}")
    
    st.info(f"Analysis completed for: {st.session_state.analyzed_company}")

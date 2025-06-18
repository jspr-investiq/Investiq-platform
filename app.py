import streamlit as st
import random

st.set_page_config(page_title="InvestIQ")
st.title("InvestIQ")

# Form
company_name = st.text_input("Company Name")
sector = st.selectbox("Sector", ["SaaS", "FinTech", "HealthTech", "AI", "Other"])
description = st.text_area("Description", height=100)

if st.button("Analyze"):
    if company_name and description:
        with st.spinner("Working..."):
            
            # Mock analysis without Claude API
            recommendations = ["INVEST", "PASS", "INVESTIGATE"]
            result = random.choice(recommendations)
            
            # Store only safe strings
            st.session_state.result = result
            st.session_state.company = company_name

# Display results
if hasattr(st.session_state, 'result'):
    if st.session_state.result == "INVEST":
        st.success(f"Recommendation: {st.session_state.result}")
    elif st.session_state.result == "PASS":
        st.error(f"Recommendation: {st.session_state.result}")
    else:
        st.warning(f"Recommendation: {st.session_state.result}")
    
    st.info(f"Analysis completed for: {st.session_state.company}")

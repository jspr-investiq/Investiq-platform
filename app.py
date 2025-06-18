import streamlit as st
import anthropic

st.set_page_config(
    page_title="InvestIQ - Professional VC Analysis",
    page_icon="💼",
    layout="wide"
)

st.title("💼 InvestIQ")
st.subheader("Professional AI-Enhanced Venture Capital Investment Analysis")

# Debug API connection
st.header("🔧 API Debug Information")

try:
    api_key = st.secrets["ANTHROPIC_API_KEY"]
    st.success(f"✅ API Key found (starts with: {api_key[:15]}...)")
    
    client = anthropic.Anthropic(api_key=api_key)
    st.success("✅ Anthropic client created successfully")
    
except KeyError:
    st.error("❌ ANTHROPIC_API_KEY not found in secrets")
    st.stop()
except Exception as e:
    st.error(f"❌ Error creating client: {str(e)}")
    st.stop()

# Simple form
st.header("📝 Investment Analysis")

company_name = st.text_input("Company Name")
sector = st.selectbox("Sector", ["SaaS/Software", "FinTech", "HealthTech", "AI/ML", "Other"])
description = st.text_area("Company Description", height=100)

if st.button("Analyze Investment"):
    if not company_name or not description:
        st.error("Please fill in company name and description")
    else:
        st.info("Starting analysis...")
        
        try:
            # Simple test prompt first
            prompt = f"Analyze this company: {company_name} in {sector}. Description: {description}. Give a brief investment recommendation."
            
            st.info("Calling Claude API...")
            
            response = client.messages.create(
                model="claude-3-sonnet-20240229",  # Using different model
                max_tokens=500,
                messages=[{"role": "user", "content": prompt}]
            )
            
            st.success("✅ API call successful!")
            
            # Display raw response for debugging
            result = response.content[0].text
            st.subheader("Analysis Result:")
            st.write(result)
            
        except Exception as e:
            st.error(f"❌ Error during analysis: {str(e)}")
            st.error(f"Error type: {type(e).__name__}")
            
            # Show more debug info
            import traceback
            st.code(traceback.format_exc())

import os
import streamlit as st
from client import get_recommendation

st.set_page_config(page_title="Agentic Refinance Tool", page_icon="🏡")

st.title("Agentic Refinance Tool")
st.caption("Hello! Use this Agentic AI powered refinance tool to determine if now is a good time for you to refinance.")

# Ensure there is a place to store the last response
if "resp" not in st.session_state:
    st.session_state.resp = None

# User Input + Basic Validation
rate_str = st.text_input("What is your current mortgage interest rate (%)", placeholder="e.g., 6.125")
current_payment_str = st.text_input("What is your current monthly mortgage payment (principal and interest only)?", placeholder="e.g., $3,350")
mortgage_balance_str = st.text_input("What is the remaining balance on your mortgage loan?", placeholder="e.g., $500,000")
run = st.button("Get recommendation")

# Show the user what API it's hitting
st.write(":wrench: API Being Used:", os.getenv("API_BASE_URL"),
         ":", os.getenv("API_PORT"),
         "/", os.getenv("API_PATH"))

def clean_strings(text: str) -> str:
    return text.strip().replace("%", "").replace("$", "")

if run:
    if not rate_str or not rate_str.strip():
        st.error("Please enter an interest rate.")
    if not current_payment_str or not current_payment_str.strip():
        st.error("Please enter a current monthly payment.")
    if not mortgage_balance_str or not mortgage_balance_str.strip():
        st.error("Please enter a mortgage balance.")
    try:
        rate=float(clean_strings(rate_str))
        current_payment=float(clean_strings(current_payment_str))
        mortgage_balance=float(clean_strings(mortgage_balance_str))
        with st.spinner("Calling agents for a recommendation..."):
            st.session_state.resp = get_recommendation(rate, current_payment, mortgage_balance)
    except ValueError:
        st.error("Please enter valid numbers only.")
        st.stop()

# Render results only if we have them
resp = st.session_state.resp
if resp:
    if "error" in resp:
        st.error(resp["error"])
    else:
        st.success("Success!")
        st.subheader("Your Refinance Recommendation: ")
        st.write(resp.get("recommendation", "-"))

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total number of agentic tools called:", resp.get("num_tool_calls", "-"))
        with col2:
            st.caption("The agentic path this workflow took is:")
            path = resp.get("path", "-")
            if isinstance(path, list):
                st.code(" -> ".join(path))
            else:
                st.code(str(path))

# RUN: poetry run streamlit run Agentic_Refinance_Tool.py

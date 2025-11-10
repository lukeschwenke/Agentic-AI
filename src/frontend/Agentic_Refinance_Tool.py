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
run = st.button("Get recommendation")

# Show the user what API it's hitting
st.write(":wrench: API Being Used:", os.getenv("API_BASE_URL"),
         ":", os.getenv("API_PORT"),
         "/", os.getenv("API_PATH"))

if run:
    if not rate_str or not rate_str.strip():
        st.error("Please enter a rate first, e.g. 6.125 or 6.125%")
    try:
        cleaned=rate_str.strip().replace("%", "")
        rate = float(cleaned)
        with st.spinner("Calling agents for a recommendation..."):
            st.session_state.resp = get_recommendation(rate)
    except ValueError:
        st.error("Please enter a valid number, e.g. 6.125 or 6.125%")
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

# Option #1: streamlit run streamlit_app.py
# Option #2: poetry run streamlit run streamlit_app.py

import streamlit as st
from pathlib import Path

st.set_page_config(page_title="Project Inspiration", layout="wide")

FRONTEND_DIR = Path(__file__).resolve().parents[1]

st.markdown("### Project Inspiration")

col_text, col_image = st.columns([2, 3])

with col_text:
    st.markdown("""
    My wife and I went through the mortgage refinancing process in fall 2025 and it was very difficult 
    to tell if it was actually an ideal time to refinance. Different lenders and people we talked to 
    suggested various criteria to weigh if refinancing was right for us. There was a big learning curve 
    but at the end of the process I felt I had a good grasp on determining if refinancing was ideal and
    decided to integrate these learnings and logic into an agentic workflow that could be leveraged by 
    myself and others in the future.
    """)

with col_image:
    IMG_PATH = FRONTEND_DIR / "images" / "inspiration_image.png"
    st.image(str(IMG_PATH), width=300)

st.markdown("### Automating Further - Daily Emails")
st.markdown("""To make refinancing in the future even easier for ourselves, I created an AWS Lambda Python script with 
            my personal mortgage details configured as environmental variables to run on a daily basis at 11:00 AM
            with the help of an AWS EventBridge Schedule. An AWS SNS Topic is in place to have the agentic
            summary emailed to me with a clear answer on whether we should refinance our mortgage.
            This is exciting because it allows us to not have 
            to watch the financial markets as closely including the 10 year treasury yield or what 
            the average interest rates people are seeing. The agents do the "hard" work!
            """)

IMG_PATH_EMAIL = FRONTEND_DIR / "images" / "refi_daily_email.png"
st.image(str(IMG_PATH_EMAIL), use_container_width=True)
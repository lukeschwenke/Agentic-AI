import streamlit as st

st.set_page_config(page_title="Project Inspiration")

st.markdown("### Project Inspiration")

st.markdown("""
    My wife and I went through the mortgage refinancing process in fall 2025 and it was very difficult 
    to tell if it was actually an ideal time to refinance. Different lenders and people we talked to 
    suggested various criteria to weigh if refinancing was right for us. There was a big learning curve 
    but at the end of the process I felt I had a good grasp on determining if refinancing was ideal and
    decided to integrate these learnings and logic into an agentic workflow that could be leveraged by 
    myself and others in the future.
    """)

st.markdown("### Additional Automation")

st.markdown("""To make refinancing in the future even easier for ourselves, I set up Apache Airflow 
            process to run this workflow once a week based on our personal financials and email me 
            a recommendation to refinance or not. This is exciting because it allows us to not have 
            to watch the financial markets as closely including the 10 year treasury yield or what 
            the average interest rates people are seeing.
            """)
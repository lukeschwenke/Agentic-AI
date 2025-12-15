import streamlit as st

st.set_page_config(page_title="Agentic Workflow Details")

st.markdown("# Agentic Workflow Details")
#st.sidebar.header("Technical Details")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""#### Agentic Workflow:""")
    st.markdown("""###### *Directed Acyclic Diagram (DAG)*""")
    from core.workflow import workflow_image
    if workflow_image is not None:
        st.image(workflow_image, width=300)
    else:
        st.info("Workflow diagram unavailable (Mermaid PNG render failed).")

with col2:
    st.markdown("""#### Overview of Agents:""")
    st.markdown("""
    ###### Agent #1 - Market Expert Agent \n 
    A mortgage market intelligence agent that aggregates and summarizes recent mortgage-rate data from multiple online sources to estimate prevailing U.S. mortgage interest rates. This agent invokes a custom tool using Tavily (web access layer for LLMs) to perform web searches and extract current market-rate signals.

    ###### Agent #2 - Treasury Yield Agent \n
    A financial data agent that retrieves the current U.S. 10-year Treasury yield via the CNBC REST API. The agent evaluates the yield relative to predefined desirability thresholds and provides contextual guidance that informs the final recommendation.
    
    ###### Agent #3 - Calculator Agent \n
    A financial calculation agent that computes the refinance breakeven period using user-provided and estimated loan data. Inputs include the user’s current monthly principal-and-interest (P&I) payment and an estimated post-refinance P&I payment. The agent calculates monthly savings, estimates closing costs, and determines the breakeven horizon as: Estimated Closing Costs ÷ Monthly Payment Savings
    
    ###### Agent #4 - Finalizer Agent \n
    A terminal agent that synthesizes outputs from the market-rate, treasury-yield, and breakeven-calculation agents to generate a concise refinance recommendation tailored to the user’s current interest rate and prevailing market conditions.
    """)

st.write("""
         Agent Code: https://github.com/lukeschwenke/Agentic-AI/blob/main/src/core/agents.py
         \nTools Code: https://github.com/lukeschwenke/Agentic-AI/blob/main/src/core/tools.py
""")
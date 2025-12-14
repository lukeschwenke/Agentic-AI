import streamlit as st

st.set_page_config(page_title="Agentic Workflow Details")

st.markdown("# Agentic Workflow Details")
#st.sidebar.header("Technical Details")

st.caption("""LangGraph Agent Diagram:""")

#st.write("")

from core.workflow import workflow_image
if workflow_image is not None:
    st.image(workflow_image, width=200)
else:
    st.info("Workflow diagram unavailable (Mermaid PNG render failed).")
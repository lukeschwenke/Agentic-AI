

from pathlib import Path
import streamlit as st

FRONTEND_DIR = Path(__file__).resolve().parents[1]
IMG_PATH = FRONTEND_DIR / "images" / "arch_diagram_v1.png"

# st.image(
#     str(IMG_PATH),
#     caption="AWS Architecture Diagram",
#     use_container_width=True
# )

st.set_page_config(layout="wide")

st.image(str(IMG_PATH), use_container_width=True)


from pathlib import Path
import streamlit as st

FRONTEND_DIR = Path(__file__).resolve().parents[1]
IMG_PATH = FRONTEND_DIR / "images" / "arch_diagram_v2.png"

st.set_page_config(layout="wide")

st.image(str(IMG_PATH), width="stretch")
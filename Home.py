import streamlit as st
from header import render_header
from sidebar import render_sidebar

st.set_page_config(page_title="Streamlit App", layout="wide")

render_header()
render_sidebar()

# =============================================================================


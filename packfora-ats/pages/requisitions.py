"""Requisitions page."""
import streamlit as st
from db import fetch
from utils.excel_loader import excel_uploader


def render():
    st.title("📋 Requisitions")
    tab1, tab2 = st.tabs(["Browse", "Import from Excel"])
    with tab1:
        df = fetch("requisitions", limit=500)
        st.dataframe(df, use_container_width=True, hide_index=True) if not df.empty else st.info("No requisitions yet.")
    with tab2:
        excel_uploader("requisitions")

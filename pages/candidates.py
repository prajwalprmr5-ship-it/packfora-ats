"""Candidates page."""
import streamlit as st
from db import fetch
from utils.excel_loader import excel_uploader


def render():
    st.title("👤 Candidates")
    tab1, tab2 = st.tabs(["Browse", "Import from Excel"])

    with tab1:
        df = fetch("candidates", limit=500)
        if df.empty:
            st.info("No candidates yet.")
        else:
            search = st.text_input("Search by name or email")
            if search and {"full_name", "email"} & set(df.columns):
                mask = False
                if "full_name" in df.columns:
                    mask = mask | df["full_name"].astype(str).str.contains(search, case=False, na=False)
                if "email" in df.columns:
                    mask = mask | df["email"].astype(str).str.contains(search, case=False, na=False)
                df = df[mask]
            st.dataframe(df, use_container_width=True, hide_index=True)

    with tab2:
        excel_uploader("candidates")

"""Dashboard page — top-level KPIs."""
import streamlit as st
import pandas as pd
from db import count, fetch


def render():
    st.title("📊 Dashboard")
    st.caption("Live snapshot of recruiting pipeline.")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Candidates", count("candidates"))
    c2.metric("Requisitions", count("requisitions"))
    c3.metric("Interviews", count("interviews"))
    c4.metric("Offers", count("offers"))

    st.divider()

    left, right = st.columns(2)
    with left:
        st.subheader("Recent Candidates")
        df = fetch("candidates", limit=8)
        st.dataframe(df, use_container_width=True, hide_index=True) if not df.empty else st.info("No candidates yet.")

    with right:
        st.subheader("Recent Requisitions")
        df = fetch("requisitions", limit=8)
        st.dataframe(df, use_container_width=True, hide_index=True) if not df.empty else st.info("No requisitions yet.")

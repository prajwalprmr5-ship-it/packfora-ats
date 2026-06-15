"""Dashboard — KPIs, status breakdowns, recent activity."""
import pandas as pd
import streamlit as st
from db import count, fetch


def render():
    st.title("📊 Dashboard")
    st.caption("Live snapshot of the recruiting pipeline.")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Candidates", count("candidates"))
    c2.metric("Requisitions", count("requisitions"))
    c3.metric("Interviews", count("interviews"))
    c4.metric("Offers", count("offers"))

    st.divider()

    # Status breakdowns
    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("Candidates by status")
        df = fetch("candidates", limit=2000, columns="candidate_status")
        if not df.empty and "candidate_status" in df.columns:
            st.bar_chart(df["candidate_status"].value_counts())
        else:
            st.info("No data.")
    with col_b:
        st.subheader("Requisitions by status")
        df = fetch("requisitions", limit=2000, columns="current_status")
        if not df.empty and "current_status" in df.columns:
            st.bar_chart(df["current_status"].value_counts())
        else:
            st.info("No data.")

    st.divider()

    left, right = st.columns(2)
    with left:
        st.subheader("Recent Candidates")
        df = fetch("candidates", limit=8)
        if df.empty:
            st.info("No candidates yet.")
        else:
            cols = [c for c in ["candidate_id", "full_name", "candidate_status", "job_name", "recruiter", "created_at"] if c in df.columns]
            st.dataframe(df[cols], use_container_width=True, hide_index=True)
    with right:
        st.subheader("Recent Requisitions")
        df = fetch("requisitions", limit=8)
        if df.empty:
            st.info("No requisitions yet.")
        else:
            cols = [c for c in ["req_id", "position_name", "current_status", "priority", "recruiter", "created_at"] if c in df.columns]
            st.dataframe(df[cols], use_container_width=True, hide_index=True)

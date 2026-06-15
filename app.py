"""Packfora ATS — main Streamlit app."""
import streamlit as st
from db import get_supabase
from pages import dashboard, candidates, requisitions, offers

st.set_page_config(page_title="Packfora ATS", layout="wide", page_icon="📋")

# --- Connection check ---
try:
    get_supabase()
except Exception as e:
    st.error(f"Failed to connect to backend: {e}")
    st.stop()

# --- Sidebar navigation ---
st.sidebar.title("📋 Packfora ATS")
PAGES = {
    "Dashboard": dashboard,
    "Candidates": candidates,
    "Requisitions": requisitions,
    "Offers": offers,
}
choice = st.sidebar.radio("Navigate", list(PAGES.keys()))
st.sidebar.divider()
st.sidebar.caption("Internal recruiting tool")

PAGES[choice].render()

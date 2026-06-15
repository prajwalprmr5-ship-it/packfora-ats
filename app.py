"""Packfora ATS — Streamlit application mirroring the web app's functionality."""
import streamlit as st
from db import get_supabase, is_authenticated, sign_in, sign_out
from pages import dashboard, candidates, requisitions, interviews, offers

st.set_page_config(page_title="Packfora ATS", layout="wide", page_icon="📋")

# Connection sanity check
try:
    get_supabase()
except Exception as e:
    st.error(f"Failed to connect to backend: {e}")
    st.stop()


def login_screen():
    st.title("📋 Packfora ATS")
    st.caption("Sign in to access the recruiting workspace.")
    with st.form("login"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Sign in", type="primary", use_container_width=True)
    if submit:
        try:
            sign_in(email, password)
            st.rerun()
        except Exception as e:
            st.error(f"Sign-in failed: {e}")


if not is_authenticated():
    login_screen()
    st.stop()

# --- Sidebar ---
st.sidebar.title("📋 Packfora ATS")
st.sidebar.caption(f"Signed in as **{st.session_state.get('user_email','')}**")

PAGES = {
    "Dashboard": dashboard,
    "Candidates": candidates,
    "Requisitions": requisitions,
    "Interviews": interviews,
    "Offers": offers,
}
choice = st.sidebar.radio("Navigate", list(PAGES.keys()))
st.sidebar.divider()
if st.sidebar.button("Sign out", use_container_width=True):
    sign_out()
    st.rerun()
st.sidebar.caption("Internal recruiting tool")

PAGES[choice].render()

"""Supabase connection & shared query helpers."""
import os
import streamlit as st
import pandas as pd
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()


# Public Supabase project credentials (publishable anon key — safe to embed).
# These are used as defaults so the app works out-of-the-box on Render/Streamlit Cloud
# without needing to configure environment variables. Override via env vars if needed.
DEFAULT_SUPABASE_URL = "https://lejtobtwavopmfgoinoh.supabase.co"
DEFAULT_SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImxlanRvYnR3YXZvcG1mZ29pbm9oIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODEwMTkzODQsImV4cCI6MjA5NjU5NTM4NH0.BtovLf0UxYranvxGhhEWH3h0_5ipexiloPdX5ZPO_v0"


@st.cache_resource
def get_supabase() -> Client:
    url = (
        os.getenv("SUPABASE_URL")
        or os.getenv("VITE_SUPABASE_URL")
        or DEFAULT_SUPABASE_URL
    )
    key = (
        os.getenv("SUPABASE_SERVICE_ROLE_KEY")
        or os.getenv("SUPABASE_PUBLISHABLE_KEY")
        or os.getenv("VITE_SUPABASE_PUBLISHABLE_KEY")
        or DEFAULT_SUPABASE_KEY
    )
    if not url or not key:
        raise RuntimeError(
            "Missing SUPABASE_URL / SUPABASE_*_KEY in environment."
        )
    return create_client(url, key)


def count(table: str) -> int:
    try:
        res = get_supabase().table(table).select("*", count="exact").limit(1).execute()
        return res.count or 0
    except Exception:
        return 0


def fetch(table: str, *, order: str = "created_at", desc: bool = True, limit: int = 100, columns: str = "*") -> pd.DataFrame:
    try:
        res = (
            get_supabase()
            .table(table)
            .select(columns)
            .order(order, desc=desc)
            .limit(limit)
            .execute()
        )
        return pd.DataFrame(res.data or [])
    except Exception as e:
        st.warning(f"Could not load {table}: {e}")
        return pd.DataFrame()


def insert(table: str, row: dict):
    return get_supabase().table(table).insert(row).execute()

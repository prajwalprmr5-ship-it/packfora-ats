"""Supabase connection & shared query helpers."""
import os
import streamlit as st
import pandas as pd
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()


@st.cache_resource
def get_supabase() -> Client:
    url = os.getenv("SUPABASE_URL") or os.getenv("VITE_SUPABASE_URL")
    key = (
        os.getenv("SUPABASE_SERVICE_ROLE_KEY")
        or os.getenv("SUPABASE_PUBLISHABLE_KEY")
        or os.getenv("VITE_SUPABASE_PUBLISHABLE_KEY")
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

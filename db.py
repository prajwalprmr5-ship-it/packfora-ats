"""Supabase connection, auth, and shared CRUD helpers."""
import os
from typing import Optional
import streamlit as st
import pandas as pd
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

# Public Supabase credentials — safe to embed (anon key).
DEFAULT_SUPABASE_URL = "https://lejtobtwavopmfgoinoh.supabase.co"
DEFAULT_SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImxlanRvYnR3YXZvcG1mZ29pbm9oIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODEwMTkzODQsImV4cCI6MjA5NjU5NTM4NH0.BtovLf0UxYranvxGhhEWH3h0_5ipexiloPdX5ZPO_v0"


def _url() -> str:
    return os.getenv("SUPABASE_URL") or os.getenv("VITE_SUPABASE_URL") or DEFAULT_SUPABASE_URL


def _key() -> str:
    return (
        os.getenv("SUPABASE_PUBLISHABLE_KEY")
        or os.getenv("VITE_SUPABASE_PUBLISHABLE_KEY")
        or os.getenv("SUPABASE_ANON_KEY")
        or DEFAULT_SUPABASE_KEY
    )


@st.cache_resource
def _anon_client() -> Client:
    return create_client(_url(), _key())


def get_supabase() -> Client:
    """Return a client. If user is signed in, attach their access token so RLS sees them."""
    client = _anon_client()
    token = st.session_state.get("access_token")
    if token:
        try:
            client.postgrest.auth(token)
        except Exception:
            pass
    return client


# ---------- Auth ----------
def sign_in(email: str, password: str):
    client = _anon_client()
    res = client.auth.sign_in_with_password({"email": email, "password": password})
    if res.session:
        st.session_state["access_token"] = res.session.access_token
        st.session_state["refresh_token"] = res.session.refresh_token
        st.session_state["user_email"] = res.user.email if res.user else email
        st.session_state["user_id"] = res.user.id if res.user else None
    return res


def sign_out():
    try:
        _anon_client().auth.sign_out()
    except Exception:
        pass
    for k in ("access_token", "refresh_token", "user_email", "user_id"):
        st.session_state.pop(k, None)


def is_authenticated() -> bool:
    return bool(st.session_state.get("access_token"))


# ---------- CRUD ----------
def count(table: str) -> int:
    try:
        res = get_supabase().table(table).select("*", count="exact").limit(1).execute()
        return res.count or 0
    except Exception:
        return 0


def count_where(table: str, column: str, value) -> int:
    try:
        res = get_supabase().table(table).select("*", count="exact").eq(column, value).limit(1).execute()
        return res.count or 0
    except Exception:
        return 0


def fetch(
    table: str,
    *,
    order: str = "created_at",
    desc: bool = True,
    limit: int = 500,
    columns: str = "*",
    filters: Optional[dict] = None,
) -> pd.DataFrame:
    try:
        q = get_supabase().table(table).select(columns)
        if filters:
            for col, val in filters.items():
                if val not in (None, "", "All"):
                    q = q.eq(col, val)
        res = q.order(order, desc=desc).limit(limit).execute()
        return pd.DataFrame(res.data or [])
    except Exception as e:
        st.warning(f"Could not load {table}: {e}")
        return pd.DataFrame()


def insert(table: str, row: dict):
    row = _clean(row)
    return get_supabase().table(table).insert(row).execute()


def insert_many(table: str, rows: list[dict]):
    rows = [_clean(r) for r in rows]
    return get_supabase().table(table).insert(rows).execute()


def update(table: str, row_id: str, row: dict, *, id_column: str = "id"):
    row = _clean(row)
    return get_supabase().table(table).update(row).eq(id_column, row_id).execute()


def delete(table: str, row_id: str, *, id_column: str = "id"):
    return get_supabase().table(table).delete().eq(id_column, row_id).execute()


def rpc(fn: str, args: Optional[dict] = None):
    return get_supabase().rpc(fn, args or {}).execute()


def _clean(row: dict) -> dict:
    """Strip empty strings to None, drop NaNs, drop None values to let DB defaults apply."""
    out = {}
    for k, v in row.items():
        if v is None:
            continue
        if isinstance(v, float) and pd.isna(v):
            continue
        if isinstance(v, str) and v.strip() == "":
            continue
        if hasattr(v, "isoformat"):
            v = v.isoformat()
        out[k] = v
    return out

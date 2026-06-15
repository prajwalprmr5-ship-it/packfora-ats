"""Reusable form/render helpers driven by schemas.py field tuples."""
from datetime import date, datetime
import pandas as pd
import streamlit as st


def _parse_date(v):
    if not v:
        return None
    if isinstance(v, (date, datetime)):
        return v if isinstance(v, date) and not isinstance(v, datetime) else v.date()
    try:
        return datetime.fromisoformat(str(v)[:10]).date()
    except Exception:
        return None


def render_form(fields, initial: dict | None = None, key_prefix: str = "f", columns: int = 2) -> dict | None:
    """Render a multi-column form from a list of field tuples.

    Returns dict of values on submit, None otherwise."""
    initial = initial or {}
    values: dict = {}
    with st.form(key=f"{key_prefix}_form", clear_on_submit=False):
        cols = st.columns(columns)
        for i, field in enumerate(fields):
            name, label, ftype, *rest = field
            opts = rest[0] if rest else None
            col = cols[i % columns]
            cur = initial.get(name)
            key = f"{key_prefix}_{name}"
            with col:
                if ftype == "text":
                    values[name] = st.text_input(label, value="" if cur is None else str(cur), key=key)
                elif ftype == "textarea":
                    values[name] = st.text_area(label, value="" if cur is None else str(cur), key=key)
                elif ftype == "select":
                    options = list(opts or [])
                    cur_str = "" if cur is None else str(cur)
                    if cur_str and cur_str not in options:
                        options = [cur_str] + options
                    idx = options.index(cur_str) if cur_str in options else 0
                    values[name] = st.selectbox(label, options, index=idx, key=key)
                elif ftype == "int":
                    try:
                        v = int(cur) if cur not in (None, "") and not pd.isna(cur) else None
                    except Exception:
                        v = None
                    values[name] = st.number_input(label, value=v if v is not None else 0, step=1, key=key) if v is not None else st.number_input(label, value=0, step=1, key=key)
                    if values[name] == 0 and v is None:
                        values[name] = None
                elif ftype == "number":
                    try:
                        v = float(cur) if cur not in (None, "") and not pd.isna(cur) else None
                    except Exception:
                        v = None
                    values[name] = st.number_input(label, value=v if v is not None else 0.0, key=key, format="%.2f")
                    if values[name] == 0.0 and v is None:
                        values[name] = None
                elif ftype == "date":
                    d = _parse_date(cur)
                    values[name] = st.date_input(label, value=d, key=key, format="YYYY-MM-DD")
        submitted = st.form_submit_button("Save", type="primary", use_container_width=True)
    if not submitted:
        return None
    # Normalize: empty strings → None, date → iso
    out: dict = {}
    for k, v in values.items():
        if isinstance(v, str) and v.strip() == "":
            out[k] = None
        elif isinstance(v, date):
            out[k] = v.isoformat()
        else:
            out[k] = v
    return out

"""Excel/CSV import helpers."""
import io
import pandas as pd
import streamlit as st
from db import insert_many


def _read(file) -> pd.DataFrame:
    name = file.name.lower()
    if name.endswith(".csv"):
        return pd.read_csv(file)
    return pd.read_excel(file)


def excel_uploader(table: str, allowed_columns: list[str] | None = None):
    st.caption("Upload .xlsx or .csv. Column headers must match table columns.")
    uploaded = st.file_uploader("File", type=["xlsx", "csv"], key=f"upload_{table}")
    if not uploaded:
        return
    try:
        df = _read(uploaded)
    except Exception as e:
        st.error(f"Could not read file: {e}")
        return

    df.columns = [str(c).strip() for c in df.columns]
    if allowed_columns:
        keep = [c for c in df.columns if c in allowed_columns]
        dropped = [c for c in df.columns if c not in allowed_columns]
        if dropped:
            st.info(f"Ignoring unknown columns: {', '.join(dropped)}")
        df = df[keep]

    st.write(f"Preview ({len(df)} rows):")
    st.dataframe(df.head(20), use_container_width=True, hide_index=True)

    if st.button(f"Import {len(df)} rows into {table}", type="primary", key=f"go_{table}"):
        rows = df.where(pd.notnull(df), None).to_dict(orient="records")
        try:
            insert_many(table, rows)
            st.success(f"Imported {len(rows)} rows into {table}.")
        except Exception as e:
            st.error(f"Import failed: {e}")


def export_csv_button(df: pd.DataFrame, filename: str, label: str = "⬇️ Export CSV"):
    if df.empty:
        return
    buf = io.StringIO()
    df.to_csv(buf, index=False)
    st.download_button(label, buf.getvalue(), file_name=filename, mime="text/csv")

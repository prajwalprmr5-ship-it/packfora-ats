"""Excel import logic — preview a sheet and bulk-insert into Supabase."""
import streamlit as st
import pandas as pd
from db import get_supabase


def read_excel(file) -> pd.DataFrame:
    return pd.read_excel(file)


def excel_uploader(table: str):
    st.subheader(f"Import to `{table}`")
    st.caption("Upload an .xlsx file. Column headers must match the table columns.")
    uploaded = st.file_uploader("Excel file", type=["xlsx"], key=f"upload_{table}")
    if not uploaded:
        return

    try:
        df = read_excel(uploaded)
    except Exception as e:
        st.error(f"Could not read Excel: {e}")
        return

    st.write(f"Preview ({len(df)} rows):")
    st.dataframe(df.head(20), use_container_width=True, hide_index=True)

    if st.button(f"Import {len(df)} rows into {table}", type="primary"):
        rows = df.where(pd.notnull(df), None).to_dict(orient="records")
        try:
            get_supabase().table(table).insert(rows).execute()
            st.success(f"Imported {len(rows)} rows into {table}.")
        except Exception as e:
            st.error(f"Import failed: {e}")

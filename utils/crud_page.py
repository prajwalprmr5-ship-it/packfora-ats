"""Reusable CRUD page builder: list + filter + add/edit/delete + import/export."""
import pandas as pd
import streamlit as st
from db import fetch, insert, update, delete, rpc
from utils.forms import render_form
from utils.excel_loader import excel_uploader, export_csv_button


def crud_page(
    *,
    title: str,
    icon: str,
    table: str,
    fields: list,
    status_field: str,
    status_options: list[str],
    id_label_field: str,
    generate_id_rpc: str | None = None,
    generate_id_arg_field: str | None = None,
    id_column_db: str = "id",
    search_fields: list[str] | None = None,
):
    st.title(f"{icon} {title}")
    tabs = st.tabs(["Browse", "Add new", "Import"])

    # --- Browse ---
    with tabs[0]:
        c1, c2 = st.columns([2, 1])
        with c2:
            status_filter = st.selectbox("Status", ["All"] + list(status_options), key=f"{table}_sf")
        with c1:
            search = st.text_input("Search", key=f"{table}_search", placeholder="Type to filter…")

        df = fetch(table, limit=1000)
        if df.empty:
            st.info(f"No {title.lower()} yet.")
        else:
            view = df.copy()
            if status_filter != "All" and status_field in view.columns:
                view = view[view[status_field] == status_filter]
            if search and search_fields:
                mask = pd.Series([False] * len(view), index=view.index)
                for f in search_fields:
                    if f in view.columns:
                        mask = mask | view[f].astype(str).str.contains(search, case=False, na=False)
                view = view[mask]

            st.caption(f"{len(view)} of {len(df)} rows")
            st.dataframe(view, use_container_width=True, hide_index=True)
            export_csv_button(view, f"{table}.csv")

            st.divider()
            st.subheader("Edit / Delete")
            label_col = id_label_field if id_label_field in view.columns else "id"
            options = {f"{row[label_col]} — {row.get('full_name') or row.get('position_name') or row.get('candidate_name') or ''}".strip(" —"): row["id"] for _, row in view.iterrows()}
            if options:
                pick = st.selectbox("Pick a record", list(options.keys()), key=f"{table}_pick")
                row_id = options[pick]
                current = view[view["id"] == row_id].iloc[0].to_dict()
                with st.expander("Edit fields", expanded=True):
                    payload = render_form(fields, initial=current, key_prefix=f"{table}_edit")
                    if payload is not None:
                        try:
                            update(table, row_id, payload)
                            st.success("Updated.")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Update failed: {e}")
                col_a, col_b = st.columns([1, 4])
                with col_a:
                    if st.button("🗑 Delete", key=f"{table}_del", type="secondary"):
                        try:
                            delete(table, row_id)
                            st.success("Deleted.")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Delete failed: {e}")

    # --- Add new ---
    with tabs[1]:
        st.caption("Required fields marked *")
        payload = render_form(fields, key_prefix=f"{table}_add")
        if payload is not None:
            # Auto-generate ID via RPC if needed (offers, interviews, candidates)
            if generate_id_rpc:
                try:
                    args = {}
                    if generate_id_arg_field:
                        args = {f"_{generate_id_arg_field}": payload.get(generate_id_arg_field) or ""}
                    res = rpc(generate_id_rpc, args)
                    new_id = res.data
                    if isinstance(new_id, list):
                        new_id = new_id[0]
                    # id column on table is candidate_id / offer_id / interview_id
                    payload[id_label_field] = new_id
                except Exception as e:
                    st.error(f"Could not generate ID: {e}")
                    return
            try:
                insert(table, payload)
                st.success("Created.")
                st.rerun()
            except Exception as e:
                st.error(f"Create failed: {e}")

    # --- Import ---
    with tabs[2]:
        allowed = [f[0] for f in fields] + [id_label_field]
        excel_uploader(table, allowed_columns=allowed)

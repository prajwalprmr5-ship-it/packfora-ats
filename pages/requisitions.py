"""Requisitions page."""
from schemas import REQUISITION_FIELDS, REQ_STATUS_OPTIONS
from utils.crud_page import crud_page


def render():
    crud_page(
        title="Requisitions",
        icon="📋",
        table="requisitions",
        fields=REQUISITION_FIELDS,
        status_field="current_status",
        status_options=REQ_STATUS_OPTIONS,
        id_label_field="req_id",
        # req_id has a DB default (generate_req_id()), no RPC needed
        search_fields=["req_id", "position_name", "client_name", "recruiter", "bu"],
    )

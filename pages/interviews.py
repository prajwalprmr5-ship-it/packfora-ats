"""Interviews page."""
from schemas import INTERVIEW_FIELDS, INTERVIEW_STATUS_OPTIONS
from utils.crud_page import crud_page


def render():
    crud_page(
        title="Interviews",
        icon="🎯",
        table="interviews",
        fields=INTERVIEW_FIELDS,
        status_field="interview_status",
        status_options=INTERVIEW_STATUS_OPTIONS,
        id_label_field="interview_id",
        generate_id_rpc="generate_interview_id",
        search_fields=["interview_id", "candidate_name", "candidate_id", "req_id", "recruiter"],
    )

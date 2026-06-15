"""Candidates page."""
from schemas import CANDIDATE_FIELDS, CANDIDATE_STATUS_OPTIONS
from utils.crud_page import crud_page


def render():
    crud_page(
        title="Candidates",
        icon="👤",
        table="candidates",
        fields=CANDIDATE_FIELDS,
        status_field="candidate_status",
        status_options=CANDIDATE_STATUS_OPTIONS,
        id_label_field="candidate_id",
        generate_id_rpc="generate_candidate_id",
        generate_id_arg_field="full_name",
        search_fields=["full_name", "email_address", "candidate_id", "job_name", "recruiter"],
    )

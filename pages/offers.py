"""Offers page."""
from schemas import OFFER_FIELDS, OFFER_STATUS_OPTIONS
from utils.crud_page import crud_page


def render():
    crud_page(
        title="Offers",
        icon="💼",
        table="offers",
        fields=OFFER_FIELDS,
        status_field="offer_status",
        status_options=OFFER_STATUS_OPTIONS,
        id_label_field="offer_id",
        generate_id_rpc="generate_offer_id",
        search_fields=["offer_id", "candidate_name", "candidate_id", "req_id", "position_name"],
    )

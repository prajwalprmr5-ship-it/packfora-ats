"""Field definitions, dropdowns, and status options mirroring the web app."""

# ---------- Candidates ----------
CANDIDATE_STATUS_OPTIONS = [
    "Applied", "Shortlisted", "Interviewed", "Offered", "Joined", "On Hold", "Rejected",
]
GENDER_OPTIONS = ["", "Male", "Female", "Other", "Prefer not to say"]

CANDIDATE_FIELDS = [
    ("full_name", "Full Name *", "text"),
    ("first_name", "First Name", "text"),
    ("last_name", "Last Name", "text"),
    ("email_address", "Email", "text"),
    ("mobile_number", "Mobile", "text"),
    ("gender", "Gender", "select", GENDER_OPTIONS),
    ("candidate_status", "Status", "select", CANDIDATE_STATUS_OPTIONS),
    ("req_id", "Req ID", "text"),
    ("fy", "FY", "text"),
    ("job_name", "Job Name", "text"),
    ("bu", "BU", "text"),
    ("job_level", "Job Level", "text"),
    ("expertise", "Expertise", "text"),
    ("client_name", "Client Name", "text"),
    ("country", "Country", "text"),
    ("location", "Location", "text"),
    ("current_location", "Current Location", "text"),
    ("recruiter", "Recruiter", "text"),
    ("linkedin_url", "LinkedIn URL", "text"),
    ("education", "Education", "text"),
    ("passout_year", "Passout Year", "int"),
    ("current_organisation", "Current Organisation", "text"),
    ("experience", "Experience (yrs)", "number"),
    ("notice_period", "Notice Period", "text"),
    ("source", "Source", "text"),
    ("source_name", "Source Name", "text"),
    ("portal_name", "Portal Name", "text"),
    ("current_ctc", "Current CTC", "number"),
    ("expected_ctc", "Expected CTC", "number"),
    ("industry_background", "Industry Background", "text"),
    ("rejection_reason", "Rejection Reason", "textarea"),
    ("recruiter_remarks", "Recruiter Remarks", "textarea"),
]

# ---------- Requisitions ----------
REQ_STATUS_OPTIONS = [
    "Open", "In Progress", "On Hold", "Offer Released", "Offer Accepted",
    "Joined", "Closed", "Cancelled", "Dead",
]
PRIORITY_OPTIONS = ["", "P0 - Critical", "P1 - High", "P2 - Medium", "P3 - Low"]
POSITION_TYPE_OPTIONS = ["", "Full-time", "Part-time", "Contract", "Intern"]
NEW_OR_REPLACEMENT_OPTIONS = ["", "New", "Replacement"]
NICHE_BAU_OPTIONS = ["", "Niche", "BAU"]

REQUISITION_FIELDS = [
    ("position_name", "Position Name *", "text"),
    ("current_status", "Status", "select", REQ_STATUS_OPTIONS),
    ("priority", "Priority", "select", PRIORITY_OPTIONS),
    ("position_type", "Position Type", "select", POSITION_TYPE_OPTIONS),
    ("new_or_replacement", "New / Replacement", "select", NEW_OR_REPLACEMENT_OPTIONS),
    ("replacement_name", "Replacement Name", "text"),
    ("niche_or_bau", "Niche / BAU", "select", NICHE_BAU_OPTIONS),
    ("fy", "FY", "text"),
    ("bu", "BU", "text"),
    ("country", "Country", "text"),
    ("location", "Location", "text"),
    ("position_level", "Position Level", "text"),
    ("client_name", "Client Name", "text"),
    ("client_manager", "Client Manager", "text"),
    ("hiring_manager", "Hiring Manager", "text"),
    ("bu_lead", "BU Lead", "text"),
    ("recruiter", "Recruiter", "text"),
    ("probable_candidate", "Probable Candidate", "text"),
    ("final_candidate", "Final Candidate", "text"),
    ("date_of_request", "Date of Request", "date"),
    ("offer_released_date", "Offer Released", "date"),
    ("offer_accepted_date", "Offer Accepted", "date"),
    ("joining_date", "Joining Date", "date"),
    ("month_of_joining", "Month of Joining", "text"),
    ("days_since_open", "Days Since Open", "int"),
    ("dead_days", "Dead Days", "int"),
    ("effective_days_since_open", "Effective Days", "int"),
    ("budget_max", "Budget Max", "number"),
    ("ctc_offered", "CTC Offered", "number"),
    ("cost_of_hire", "Cost of Hire", "number"),
    ("passout_year", "Passout Year", "int"),
    ("source", "Source", "text"),
    ("root_cause_category", "Root Cause Category", "text"),
    ("reason", "Reason", "textarea"),
    ("remarks", "Remarks", "textarea"),
]

# ---------- Interviews ----------
INTERVIEW_STATUS_OPTIONS = [
    "Scheduled", "R1 Cleared", "R2 Cleared", "R3 Cleared",
    "Selected", "Rejected", "On Hold", "No Show", "Withdrawn",
]
FEEDBACK_OPTIONS = ["", "Selected", "Rejected", "On Hold", "Pending", "No Show"]

INTERVIEW_FIELDS = [
    ("candidate_id", "Candidate ID *", "text"),
    ("candidate_name", "Candidate Name", "text"),
    ("req_id", "Req ID", "text"),
    ("job_name", "Job Name", "text"),
    ("job_level", "Job Level", "text"),
    ("bu", "BU", "text"),
    ("recruiter", "Recruiter", "text"),
    ("interview_status", "Status", "select", INTERVIEW_STATUS_OPTIONS),
    ("r1_date", "R1 Date", "date"),
    ("r1_panel", "R1 Panel", "text"),
    ("r1_feedback", "R1 Feedback", "select", FEEDBACK_OPTIONS),
    ("r2_date", "R2 Date", "date"),
    ("r2_panel", "R2 Panel", "text"),
    ("r2_feedback", "R2 Feedback", "select", FEEDBACK_OPTIONS),
    ("r3_date", "R3 Date", "date"),
    ("r3_panel", "R3 Panel", "text"),
    ("r3_feedback", "R3 Feedback", "select", FEEDBACK_OPTIONS),
    ("remarks", "Remarks", "textarea"),
]

# ---------- Offers ----------
OFFER_STATUS_OPTIONS = ["Released", "Accepted", "Declined", "Joined"]

OFFER_FIELDS = [
    ("candidate_id", "Candidate ID *", "text"),
    ("candidate_name", "Candidate Name", "text"),
    ("req_id", "Req ID", "text"),
    ("position_name", "Position Name", "text"),
    ("recruiter", "Recruiter", "text"),
    ("offer_status", "Status", "select", OFFER_STATUS_OPTIONS),
    ("offer_released_date", "Offer Released", "date"),
    ("offer_accepted_date", "Offer Accepted", "date"),
    ("joining_date", "Joining Date", "date"),
    ("ctc_offered", "CTC Offered", "number"),
]

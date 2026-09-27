"""Shared constants and formatting helpers used across pages."""

MAIN_DISCLAIMER = (
    "This application provides informational recommendations based on the information "
    "entered by the user. Eligibility shown here is not an official government determination. "
    "Scheme details and eligibility requirements should be verified with the relevant official "
    "government source before applying."
)

SYNTHETIC_DATA_NOTICE = (
    "Synthetic demonstration data — verify scheme details with official government sources "
    "before applying. Some scheme records are synthetic data created for demonstration purposes."
)

ALL_DOCUMENTS = [
    "Aadhaar Card",
    "Income Certificate",
    "Caste Certificate",
    "Residence Certificate",
    "Bank Account",
    "Student ID",
    "Disability Certificate",
    "Land Records",
    "PAN Card",
    "Ration Card",
    "Age Proof",
    "Birth Certificate",
    "Business Plan",
    "Education Certificates",
    "Mark Sheets",
    "Employment Exchange Registration",
    "Job Card",
    "Pregnancy Certificate",
    "Death Certificate of Spouse",
    "Resume/Education Certificates",
]

STATES_LIST = [
    "Tamil Nadu", "Kerala", "Karnataka", "Andhra Pradesh", "Telangana",
    "Maharashtra", "Gujarat", "Rajasthan", "Uttar Pradesh", "Bihar",
    "West Bengal", "Madhya Pradesh", "Punjab", "Haryana", "Odisha",
    "Assam", "Jharkhand", "Chhattisgarh", "Delhi", "Other",
]


def format_currency(value):
    if value is None:
        return "No limit"
    try:
        return f"₹{int(value):,}"
    except (ValueError, TypeError):
        return str(value)


def status_label(score):
    """Wording deliberately avoids implying an official decision."""
    if score >= 80:
        return "Likely Eligible", "🟢"
    if score >= 50:
        return "Partially Eligible", "🟡"
    return "Possibly Not Eligible", "🔴"


def demo_profile():
    return {
        "name": "Demo User",
        "age": 21,
        "gender": "female",
        "state": "Tamil Nadu",
        "district": "Chennai",
        "income": 180000,
        "employment_status": "unemployed",
        "occupation": "Student",
        "is_student": True,
        "is_farmer": False,
        "has_disability": False,
        "is_rural": False,
        "marital_status": "Single",
        "family_size": 4,
        "education_level": "Undergraduate",
        "is_entrepreneur": False,
        "social_category": "General",
        "documents": {
            "Aadhaar Card": True,
            "Income Certificate": False,
            "Student ID": True,
            "Bank Account": True,
        },
    }

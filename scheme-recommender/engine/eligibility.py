"""Per-criterion eligibility checks.
Each check returns a dict: {criterion, applicable, passed, message}.
'applicable' = False means the scheme does not restrict on this criterion,
so it is excluded from scoring and from matched/failed lists.
If required profile info is missing/None, applicable=True but passed=None
(treated as 'missing info', not a failure).
"""


def _missing(criterion, label):
    return {"criterion": criterion, "applicable": True, "passed": None,
            "message": f"{label} not provided — cannot verify"}


def check_age(scheme, profile):
    age_min, age_max = scheme.get("age_min"), scheme.get("age_max")
    if age_min is None and age_max is None:
        return {"criterion": "age", "applicable": False, "passed": None, "message": ""}
    age = profile.get("age")
    if age is None:
        return _missing("age", "Age")
    ok = True
    if age_min is not None and age < age_min:
        ok = False
    if age_max is not None and age > age_max:
        ok = False
    msg = f"Age {age} within required range ({age_min or 0}-{age_max or '∞'})" if ok else \
        f"Age {age} outside required range ({age_min or 0}-{age_max or '∞'})"
    return {"criterion": "age", "applicable": True, "passed": ok, "message": msg}


def check_gender(scheme, profile):
    g = scheme.get("gender", "any")
    if not g or g == "any":
        return {"criterion": "gender", "applicable": False, "passed": None, "message": ""}
    user_g = profile.get("gender")
    if not user_g:
        return _missing("gender", "Gender")
    ok = user_g.lower() == g.lower()
    msg = "Gender requirement satisfied" if ok else f"Scheme requires gender: {g}"
    return {"criterion": "gender", "applicable": True, "passed": ok, "message": msg}


def check_income(scheme, profile):
    limit = scheme.get("income_limit")
    if limit is None:
        return {"criterion": "income", "applicable": False, "passed": None, "message": ""}
    income = profile.get("income")
    if income is None:
        return _missing("income", "Annual income")
    ok = income <= limit
    msg = f"Income within limit ({limit:,})" if ok else f"Income exceeds limit ({limit:,})"
    return {"criterion": "income", "applicable": True, "passed": ok, "message": msg}


def check_state(scheme, profile):
    states = scheme.get("states", ["All"])
    if not states or "All" in states:
        return {"criterion": "state", "applicable": False, "passed": None, "message": ""}
    user_state = profile.get("state")
    if not user_state:
        return _missing("state", "State")
    ok = user_state in states
    msg = "State eligible" if ok else f"Scheme only available in: {', '.join(states)}"
    return {"criterion": "state", "applicable": True, "passed": ok, "message": msg}


def check_occupation(scheme, profile):
    occ = scheme.get("occupation", "any")
    if not occ or occ == "any":
        return {"criterion": "occupation", "applicable": False, "passed": None, "message": ""}
    user_occ = profile.get("occupation")
    if not user_occ:
        return _missing("occupation", "Occupation")
    ok = user_occ.strip().lower() == occ.strip().lower()
    msg = "Occupation matches" if ok else f"Scheme requires occupation: {occ}"
    return {"criterion": "occupation", "applicable": True, "passed": ok, "message": msg}


def check_student(scheme, profile):
    if not scheme.get("student_required"):
        return {"criterion": "student", "applicable": False, "passed": None, "message": ""}
    is_student = profile.get("is_student")
    if is_student is None:
        return _missing("student", "Student status")
    msg = "Student requirement satisfied" if is_student else "Scheme requires student status"
    return {"criterion": "student", "applicable": True, "passed": bool(is_student), "message": msg}


def check_farmer(scheme, profile):
    if not scheme.get("farmer_required"):
        return {"criterion": "farmer", "applicable": False, "passed": None, "message": ""}
    is_farmer = profile.get("is_farmer")
    if is_farmer is None:
        return _missing("farmer", "Farmer status")
    msg = "Farmer requirement satisfied" if is_farmer else "Scheme requires farmer status"
    return {"criterion": "farmer", "applicable": True, "passed": bool(is_farmer), "message": msg}


def check_employment_status(scheme, profile):
    status = scheme.get("employment_status", "any")
    if not status or status == "any":
        return {"criterion": "employment_status", "applicable": False, "passed": None, "message": ""}
    user_status = profile.get("employment_status")
    if not user_status:
        return _missing("employment_status", "Employment status")
    ok = user_status.strip().lower() == status.strip().lower()
    msg = "Employment status matches" if ok else f"Scheme requires employment status: {status}"
    return {"criterion": "employment_status", "applicable": True, "passed": ok, "message": msg}


def check_disability(scheme, profile):
    if not scheme.get("disability_required"):
        return {"criterion": "disability", "applicable": False, "passed": None, "message": ""}
    has_disability = profile.get("has_disability")
    if has_disability is None:
        return _missing("disability", "Disability status")
    msg = "Disability requirement satisfied" if has_disability else "Scheme requires disability certification"
    return {"criterion": "disability", "applicable": True, "passed": bool(has_disability), "message": msg}


def check_rural(scheme, profile):
    if not scheme.get("rural_required"):
        return {"criterion": "rural", "applicable": False, "passed": None, "message": ""}
    is_rural = profile.get("is_rural")
    if is_rural is None:
        return _missing("rural", "Rural/urban status")
    msg = "Rural requirement satisfied" if is_rural else "Scheme requires rural residence"
    return {"criterion": "rural", "applicable": True, "passed": bool(is_rural), "message": msg}


def check_education_level(scheme, profile):
    level = scheme.get("education_level", "any")
    if not level or level == "any":
        return {"criterion": "education_level", "applicable": False, "passed": None, "message": ""}
    allowed = level if isinstance(level, list) else [level]
    user_level = profile.get("education_level")
    if not user_level:
        return _missing("education_level", "Education level")
    ok = user_level in allowed
    msg = "Education level matches" if ok else f"Scheme requires education level: {', '.join(allowed)}"
    return {"criterion": "education_level", "applicable": True, "passed": ok, "message": msg}


ALL_CHECKS = [
    check_age, check_gender, check_income, check_state, check_occupation,
    check_student, check_farmer, check_employment_status, check_disability,
    check_rural, check_education_level,
]


def run_all_checks(scheme, profile):
    return [check(scheme, profile) for check in ALL_CHECKS]

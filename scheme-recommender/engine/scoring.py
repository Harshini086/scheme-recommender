"""Transparent scoring: score = passed applicable criteria / total applicable criteria.
Missing-info criteria count as 'not yet passed' but are reported separately so the
UI can distinguish 'failed' from 'unknown because info is missing'."""


def calculate_match(check_results):
    applicable = [c for c in check_results if c["applicable"]]
    if not applicable:
        return 100  # fully open scheme, nothing restricts it
    passed = [c for c in applicable if c["passed"] is True]
    score = round(len(passed) / len(applicable) * 100)
    return score


def split_results(check_results):
    """Returns (matched, failed, missing_info) lists of messages."""
    matched, failed, missing_info = [], [], []
    for c in check_results:
        if not c["applicable"]:
            continue
        if c["passed"] is True:
            matched.append(c["message"])
        elif c["passed"] is False:
            failed.append(c["message"])
        else:
            missing_info.append(c["message"])
    return matched, failed, missing_info

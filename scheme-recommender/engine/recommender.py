"""Orchestrates the recommendation pipeline. UI code should only call
get_recommendations() / evaluate_scheme() — never touch eligibility/scoring directly.
This keeps the engine swappable/independent from the UI and from the data source."""
from engine.eligibility import run_all_checks
from engine.scoring import calculate_match, split_results


def get_missing_documents(scheme, profile):
    required = scheme.get("documents_required", [])
    have = profile.get("documents", {}) or {}
    missing = [d for d in required if not have.get(d, False)]
    return missing


def evaluate_scheme(scheme, profile):
    """Returns a full evaluation dict for a single scheme against a profile."""
    checks = run_all_checks(scheme, profile)
    score = calculate_match(checks)
    matched, failed, missing_info = split_results(checks)
    missing_docs = get_missing_documents(scheme, profile)

    return {
        "scheme": scheme,
        "score": score,
        "matched": matched,
        "failed": failed,
        "missing_info": missing_info,
        "missing_docs": missing_docs,
        "docs_ready": len(scheme.get("documents_required", [])) - len(missing_docs),
        "docs_total": len(scheme.get("documents_required", [])),
    }


def get_recommendations(profile, schemes, min_score=0):
    """Ranked list of scheme evaluations, highest match first."""
    if not profile or not schemes:
        return []
    results = [evaluate_scheme(s, profile) for s in schemes]
    results = [r for r in results if r["score"] >= min_score]
    results.sort(key=lambda r: (r["score"], -len(r["missing_docs"])), reverse=True)
    return results


def find_scheme_by_id(scheme_id, schemes):
    for s in schemes:
        if s.get("scheme_id") == scheme_id:
            return s
    return None

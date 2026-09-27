import os
import streamlit as st
from utils.data_loader import load_schemes
from utils.helpers import MAIN_DISCLAIMER
from engine.recommender import get_recommendations

st.set_page_config(page_title="Scheme Assistant — SchemeSetu", page_icon="💬", layout="wide")
st.title("💬 Scheme Assistant")
st.caption("Ask about schemes, eligibility, or documents. Answers are generated from the local scheme dataset.")

schemes, err = load_schemes()
if err:
    st.error(err)
    st.stop()

profile = st.session_state.get("profile")


# ---------------- Deterministic fallback logic ----------------
def _schemes_by_flag(flag_key, value=True):
    return [s for s in schemes if s.get(flag_key) == value]


def _schemes_by_category_keyword(keyword):
    keyword = keyword.lower()
    return [s for s in schemes if keyword in s["category"].lower()]


def _format_scheme_list(matches, limit=8):
    if not matches:
        return "I couldn't find any matching schemes in the dataset."
    lines = [f"- **{s['scheme_name']}** ({s['category']}) — {s.get('benefits','')}" for s in matches[:limit]]
    return "\n".join(lines)


def fallback_answer(query):
    q = query.lower()

    if "student" in q:
        return "Schemes for students:\n" + _format_scheme_list(_schemes_by_flag("student_required"))

    if "women" in q or "woman" in q or "girl" in q:
        return "Schemes focused on women:\n" + _format_scheme_list([s for s in schemes if s.get("gender") == "female"])

    if "farmer" in q or "agriculture" in q:
        return "Schemes for farmers:\n" + _format_scheme_list(_schemes_by_flag("farmer_required"))

    if "disab" in q:
        return "Disability support schemes:\n" + _format_scheme_list(_schemes_by_flag("disability_required"))

    if "senior" in q or "elderly" in q or "old age" in q:
        return "Senior citizen schemes:\n" + _format_scheme_list(_schemes_by_category_keyword("senior"))

    if "document" in q:
        if profile:
            recs = get_recommendations(profile, schemes)
            missing = set()
            for r in recs:
                missing.update(r["missing_docs"])
            if missing:
                return "Based on your current recommendations, you still need: " + ", ".join(sorted(missing))
            return "Great news — you already have all documents required by your current recommended schemes!"
        return "Fill in your profile first so I can tell you which documents you specifically need."

    if "why" in q and ("recommend" in q or "eligib" in q or "match" in q):
        return ("Recommendations are based on matching your profile (age, income, state, "
                "occupation, student/farmer/disability/rural status, etc.) against each scheme's "
                "configured eligibility rules. Open a scheme's 'View Details' page to see exactly "
                "which criteria you matched or missed.")

    if "improve" in q and "eligib" in q:
        return ("To improve your eligibility matches: 1) Complete all profile fields — missing "
                "info can't be verified. 2) Gather commonly required documents like Aadhaar Card, "
                "Income Certificate and Bank Account. 3) Check the Documents page to see which "
                "documents are needed by the most schemes.")

    for category in {s["category"] for s in schemes}:
        if category.lower() in q:
            return f"{category} schemes:\n" + _format_scheme_list(_schemes_by_category_keyword(category))

    # keyword search against scheme names/descriptions as last resort
    matches = [s for s in schemes if q.strip() and (q in s["scheme_name"].lower() or q in s.get("description", "").lower())]
    if matches:
        return "Here's what I found:\n" + _format_scheme_list(matches)

    return ("I can help with questions like: 'schemes for students', 'schemes for women', "
            "'schemes for farmers', 'what documents do I need', 'show me education schemes', "
            "or 'why was this scheme recommended'. Try rephrasing your question.")


# ---------------- Optional LLM integration ----------------
def llm_available():
    return bool(os.environ.get("ANTHROPIC_API_KEY") or os.environ.get("OPENAI_API_KEY"))


def llm_answer(query):
    """Best-effort LLM call. Falls back silently to deterministic answer on any failure."""
    try:
        import anthropic  # optional dependency, only needed if API key is set
        client = anthropic.Anthropic()
        context = "\n".join(f"{s['scheme_name']} ({s['category']}): {s.get('description','')}" for s in schemes)
        msg = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=400,
            messages=[{"role": "user", "content":
                f"You are a government scheme assistant. Use ONLY this scheme data:\n{context}\n\n"
                f"Answer briefly and clearly: {query}"}],
        )
        return msg.content[0].text
    except Exception:
        return None


if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if not llm_available():
    st.caption("ℹ️ Running in local fallback mode (no LLM API key configured) — answers come directly from the scheme dataset.")

for role, text in st.session_state.chat_history:
    with st.chat_message(role):
        st.markdown(text)

query = st.chat_input("Ask about schemes, eligibility, or documents...")
if query:
    st.session_state.chat_history.append(("user", query))
    with st.chat_message("user"):
        st.markdown(query)

    answer = None
    if llm_available():
        answer = llm_answer(query)
    if not answer:
        answer = fallback_answer(query)

    st.session_state.chat_history.append(("assistant", answer))
    with st.chat_message("assistant"):
        st.markdown(answer)

st.divider()
st.caption(MAIN_DISCLAIMER)

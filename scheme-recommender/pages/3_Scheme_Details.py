import streamlit as st
from utils.data_loader import load_schemes
from utils.helpers import MAIN_DISCLAIMER, format_currency, status_label
from engine.recommender import find_scheme_by_id, evaluate_scheme

st.set_page_config(page_title="Scheme Details — SchemeSetu", page_icon="📄", layout="wide")

schemes, err = load_schemes()
if err:
    st.error(err)
    st.stop()

scheme_id = st.session_state.get("selected_scheme_id")
if not scheme_id:
    st.warning("No scheme selected. Go to Dashboard or Browse Schemes and click 'View Details'.")
    st.stop()

s = find_scheme_by_id(scheme_id, schemes)
if not s:
    st.error("Scheme not found.")
    st.stop()

st.title(s["scheme_name"])
st.caption(s["category"])
if s.get("is_synthetic"):
    st.caption("🔖 Synthetic demo record")

st.markdown(f"**Description:** {s.get('description','')}")
st.markdown(f"**Benefits:** {s.get('benefits','')}")

with st.expander("📋 Eligibility criteria (as configured)"):
    st.write(f"- Age: {s.get('age_min','—')} to {s.get('age_max','—')}")
    st.write(f"- Gender: {s.get('gender','any')}")
    st.write(f"- Income limit: {format_currency(s.get('income_limit'))}")
    st.write(f"- States: {', '.join(s.get('states', ['All']))}")
    st.write(f"- Student required: {s.get('student_required')}")
    st.write(f"- Farmer required: {s.get('farmer_required')}")
    st.write(f"- Disability required: {s.get('disability_required')}")
    st.write(f"- Rural required: {s.get('rural_required')}")

st.divider()

profile = st.session_state.get("profile")
if profile:
    result = evaluate_scheme(s, profile)
    label, emoji = status_label(result["score"])
    st.subheader(f"Your Match: {result['score']}% — {emoji} {label}")
    st.caption("Potentially eligible based on the information provided — not an official determination.")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Why you may qualify**")
        if result["matched"]:
            for m in result["matched"]:
                st.write(f"✓ {m}")
        else:
            st.write("—")
    with col2:
        st.markdown("**What is missing / does not match**")
        if result["failed"]:
            for f in result["failed"]:
                st.write(f"✗ {f}")
        if result["missing_info"]:
            for m in result["missing_info"]:
                st.write(f"⚠ {m}")
        if not result["failed"] and not result["missing_info"]:
            st.write("—")

    st.markdown("**Documents**")
    have = profile.get("documents", {})
    for doc in s.get("documents_required", []):
        checked = "☑" if have.get(doc) else "☐"
        st.write(f"{checked} {doc}")
else:
    st.info("Fill in your profile to see a personalized eligibility explanation.")
    st.markdown("**Required documents:**")
    for doc in s.get("documents_required", []):
        st.write(f"- {doc}")

st.divider()
st.markdown(f"**Application method:** {s.get('application_method','—')}")
st.markdown(f"**Official source note:** {s.get('official_source','—')}")
st.caption(MAIN_DISCLAIMER)

if st.button("← Back to Dashboard"):
    st.switch_page("pages/1_Dashboard.py")

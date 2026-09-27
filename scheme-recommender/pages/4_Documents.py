import streamlit as st
from utils.data_loader import load_schemes
from utils.helpers import ALL_DOCUMENTS, MAIN_DISCLAIMER
from engine.recommender import get_recommendations

st.set_page_config(page_title="Documents — SchemeSetu", page_icon="📁", layout="wide")
st.title("📁 Document Readiness")

profile = st.session_state.get("profile")
if not profile:
    st.warning("No profile found yet. Please fill in your details first.")
    if st.button("Go to Profile Form"):
        st.switch_page("app.py")
    st.stop()

schemes, err = load_schemes()
if err:
    st.error(err)
    st.stop()

have = profile.get("documents", {})

# Update documents live on this page
st.subheader("Update your documents")
cols = st.columns(3)
for i, doc in enumerate(ALL_DOCUMENTS):
    have[doc] = cols[i % 3].checkbox(doc, value=have.get(doc, False), key=f"doc_{doc}")
profile["documents"] = have
st.session_state.profile = profile

st.divider()

recs = get_recommendations(profile, schemes)
required_docs = set()
for r in recs:
    required_docs.update(r["scheme"].get("documents_required", []))

if not required_docs:
    st.info("No document requirements found for your current recommendations.")
    st.stop()

ready = [d for d in required_docs if have.get(d)]
missing = [d for d in required_docs if not have.get(d)]
readiness_pct = round(len(ready) / len(required_docs) * 100)

st.subheader(f"{readiness_pct}% Document Ready")
st.progress(readiness_pct / 100)

c1, c2 = st.columns(2)
with c1:
    st.markdown("**✅ Documents you have**")
    for d in sorted(ready):
        st.write(f"☑ {d}")
with c2:
    st.markdown("**⚠ Documents still needed**")
    for d in sorted(missing):
        st.write(f"☐ {d}")

if missing:
    # Prioritize by how many recommended schemes need each missing doc
    priority = sorted(missing, key=lambda d: -sum(1 for r in recs if d in r["scheme"].get("documents_required", [])))
    st.markdown("**📌 Get these first (needed by the most schemes):**")
    for d in priority[:3]:
        count = sum(1 for r in recs if d in r["scheme"].get("documents_required", []))
        st.write(f"- {d} (needed by {count} scheme(s))")

st.divider()
st.caption(MAIN_DISCLAIMER)

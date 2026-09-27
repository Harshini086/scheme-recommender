import streamlit as st
from utils.data_loader import load_schemes
from utils.helpers import MAIN_DISCLAIMER, SYNTHETIC_DATA_NOTICE, status_label
from engine.recommender import get_recommendations

st.set_page_config(page_title="Dashboard — SchemeSetu", page_icon="📊", layout="wide")
st.title("📊 Your Recommendation Dashboard")

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

recs = get_recommendations(profile, schemes)

# ---------- Summary cards ----------
high_match = [r for r in recs if r["score"] >= 80]
total_docs_required = sum(r["docs_total"] for r in recs) or 1
total_docs_ready = sum(r["docs_ready"] for r in recs)
total_docs_missing = total_docs_required - total_docs_ready

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Schemes Found", len(recs))
c2.metric("High Match (≥80%)", len(high_match))
c3.metric("Documents Ready", total_docs_ready)
c4.metric("Documents Missing", total_docs_missing)
c5.metric("Overall Doc Readiness", f"{round(total_docs_ready/total_docs_required*100)}%")

st.info(SYNTHETIC_DATA_NOTICE, icon="ℹ️")

# ---------- Filters ----------
with st.expander("🔍 Refine results"):
    min_score = st.slider("Minimum match %", 0, 100, 0, step=10)
    recs = [r for r in recs if r["score"] >= min_score]

st.subheader(f"Recommended Schemes ({len(recs)})")

if not recs:
    st.warning("No schemes matched. Try lowering the minimum match % filter above.")

for r in recs:
    s = r["scheme"]
    label, emoji = status_label(r["score"])
    with st.container(border=True):
        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown(f"### {s['scheme_name']}")
            st.caption(f"{s['category']}  •  {s.get('description','')}")
            st.markdown(f"**Benefit:** {s.get('benefits','')}")
        with col2:
            st.metric("Match", f"{r['score']}%")
            st.markdown(f"{emoji} **{label}**")

        if r["missing_docs"]:
            st.warning("⚠ Missing documents: " + ", ".join(r["missing_docs"]))
        else:
            st.success("✅ All required documents available")

        b1, b2 = st.columns([1, 5])
        if b1.button("View Details", key=f"view_{s['scheme_id']}"):
            st.session_state.selected_scheme_id = s["scheme_id"]
            st.switch_page("pages/3_Scheme_Details.py")

st.divider()
st.caption(MAIN_DISCLAIMER)

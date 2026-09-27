import streamlit as st
from utils.helpers import MAIN_DISCLAIMER, SYNTHETIC_DATA_NOTICE, ALL_DOCUMENTS, STATES_LIST, demo_profile
from utils.data_loader import load_schemes

st.set_page_config(page_title="SchemeSetu", page_icon="🏛️", layout="wide")

if "profile" not in st.session_state:
    st.session_state.profile = {}
if "step" not in st.session_state:
    st.session_state.step = 1

schemes, load_err = load_schemes()

# ---------- Header ----------
st.title("🏛️ SchemeSetu")
st.caption("Find government schemes you may be eligible for.")
st.info(SYNTHETIC_DATA_NOTICE, icon="ℹ️")

if load_err:
    st.error(f"Could not load scheme data: {load_err}")
    st.stop()

col_a, col_b = st.columns([3, 1])
with col_b:
    if st.button("⚡ Load Demo Profile", use_container_width=True):
        st.session_state.profile = demo_profile()
        st.session_state.step = 5
        st.rerun()

st.divider()

TOTAL_STEPS = 5
st.progress(st.session_state.step / TOTAL_STEPS, text=f"Step {st.session_state.step} of {TOTAL_STEPS}")

p = st.session_state.profile

# ---------- STEP 1: Basic Information ----------
if st.session_state.step == 1:
    st.subheader("Step 1 — Basic Information")
    p["name"] = st.text_input("Name (optional)", value=p.get("name", ""))
    c1, c2 = st.columns(2)
    p["age"] = c1.number_input("Age", min_value=0, max_value=120, value=p.get("age", 25))
    p["gender"] = c2.selectbox("Gender", ["male", "female", "other"],
                                index=["male", "female", "other"].index(p.get("gender", "male")))
    c3, c4 = st.columns(2)
    p["state"] = c3.selectbox("State", STATES_LIST, index=STATES_LIST.index(p["state"]) if p.get("state") in STATES_LIST else 0)
    p["district"] = c4.text_input("District (optional)", value=p.get("district", ""))
    if st.button("Next →", type="primary"):
        st.session_state.step = 2
        st.rerun()

# ---------- STEP 2: Financial Information ----------
elif st.session_state.step == 2:
    st.subheader("Step 2 — Financial Information")
    p["income"] = st.number_input("Annual household income (₹)", min_value=0, value=p.get("income", 200000), step=10000)
    c1, c2 = st.columns(2)
    p["employment_status"] = c1.selectbox("Employment status",
        ["employed", "unemployed", "self-employed", "retired", "any"],
        index=["employed", "unemployed", "self-employed", "retired", "any"].index(p.get("employment_status", "unemployed")))
    p["occupation"] = c2.text_input("Occupation (e.g. Student, Farmer, Business)", value=p.get("occupation", ""))
    c3, c4 = st.columns(2)
    if c3.button("← Back"):
        st.session_state.step = 1
        st.rerun()
    if c4.button("Next →", type="primary"):
        st.session_state.step = 3
        st.rerun()

# ---------- STEP 3: Personal Situation ----------
elif st.session_state.step == 3:
    st.subheader("Step 3 — Personal Situation")
    c1, c2 = st.columns(2)
    p["is_student"] = c1.checkbox("I am currently a student", value=p.get("is_student", False))
    p["is_farmer"] = c2.checkbox("I am a farmer", value=p.get("is_farmer", False))
    c3, c4 = st.columns(2)
    p["has_disability"] = c3.checkbox("I have a certified disability", value=p.get("has_disability", False))
    p["is_rural"] = c4.checkbox("I live in a rural area", value=p.get("is_rural", False))
    c5, c6 = st.columns(2)
    p["marital_status"] = c5.selectbox("Marital status", ["Single", "Married", "Widowed", "Other"],
        index=["Single", "Married", "Widowed", "Other"].index(p.get("marital_status", "Single")))
    p["family_size"] = c6.number_input("Family size", min_value=1, max_value=20, value=p.get("family_size", 4))
    p["social_category"] = st.selectbox("Social category", ["General", "OBC", "SC", "ST", "Other"],
        index=["General", "OBC", "SC", "ST", "Other"].index(p.get("social_category", "General")))
    c7, c8 = st.columns(2)
    if c7.button("← Back"):
        st.session_state.step = 2
        st.rerun()
    if c8.button("Next →", type="primary"):
        st.session_state.step = 4
        st.rerun()

# ---------- STEP 4: Education & Career ----------
elif st.session_state.step == 4:
    st.subheader("Step 4 — Education & Career")
    edu_options = ["Below 10th", "10th Pass", "12th Pass", "Undergraduate", "Graduate", "Postgraduate", "Other"]
    p["education_level"] = st.selectbox("Highest education level", edu_options,
        index=edu_options.index(p.get("education_level", "12th Pass")) if p.get("education_level") in edu_options else 2)
    p["is_entrepreneur"] = st.checkbox("I run or plan to run a business", value=p.get("is_entrepreneur", False))
    c1, c2 = st.columns(2)
    if c1.button("← Back"):
        st.session_state.step = 3
        st.rerun()
    if c2.button("Next →", type="primary"):
        st.session_state.step = 5
        st.rerun()

# ---------- STEP 5: Documents ----------
elif st.session_state.step == 5:
    st.subheader("Step 5 — Documents You Already Have")
    docs = p.get("documents", {})
    cols = st.columns(2)
    for i, doc in enumerate(ALL_DOCUMENTS[:10]):
        docs[doc] = cols[i % 2].checkbox(doc, value=docs.get(doc, False))
    p["documents"] = docs
    c1, c2 = st.columns(2)
    if c1.button("← Back"):
        st.session_state.step = 4
        st.rerun()
    if c2.button("✅ Get My Recommendations", type="primary"):
        st.session_state.profile = p
        st.switch_page("pages/1_Dashboard.py")

st.divider()
st.caption(MAIN_DISCLAIMER)

import streamlit as st
from utils.data_loader import load_schemes, get_categories, get_states
from utils.helpers import SYNTHETIC_DATA_NOTICE, MAIN_DISCLAIMER

st.set_page_config(page_title="Browse Schemes — SchemeSetu", page_icon="🔎", layout="wide")
st.title("🔎 Browse & Search Schemes")
st.info(SYNTHETIC_DATA_NOTICE, icon="ℹ️")

schemes, err = load_schemes()
if err:
    st.error(err)
    st.stop()

categories = ["All"] + get_categories(schemes)
states = ["All"] + get_states(schemes)

c1, c2, c3 = st.columns(3)
keyword = c1.text_input("Search by name or keyword")
category = c2.selectbox("Category", categories)
state = c3.selectbox("State", states)

c4, c5, c6 = st.columns(3)
student_only = c4.checkbox("Student schemes only")
farmer_only = c5.checkbox("Farmer schemes only")
women_only = c6.checkbox("Women-focused schemes only")

c7, c8 = st.columns(2)
disability_only = c7.checkbox("Disability support only")
rural_only = c8.checkbox("Rural-only schemes")

filtered = []
for s in schemes:
    if keyword and keyword.lower() not in s["scheme_name"].lower() and keyword.lower() not in s.get("description", "").lower():
        continue
    if category != "All" and s["category"] != category:
        continue
    if state != "All" and "All" not in s.get("states", []) and state not in s.get("states", []):
        continue
    if student_only and not s.get("student_required"):
        continue
    if farmer_only and not s.get("farmer_required"):
        continue
    if women_only and s.get("gender") != "female":
        continue
    if disability_only and not s.get("disability_required"):
        continue
    if rural_only and not s.get("rural_required"):
        continue
    filtered.append(s)

st.subheader(f"{len(filtered)} scheme(s) found")

for s in filtered:
    with st.container(border=True):
        st.markdown(f"### {s['scheme_name']}")
        st.caption(s["category"])
        st.write(s.get("description", ""))
        st.markdown(f"**Benefit:** {s.get('benefits','')}")
        if st.button("View Details", key=f"browse_{s['scheme_id']}"):
            st.session_state.selected_scheme_id = s["scheme_id"]
            st.switch_page("pages/3_Scheme_Details.py")

st.divider()
st.caption(MAIN_DISCLAIMER)

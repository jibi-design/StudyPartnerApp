import streamlit as st
from pathlib import Path
import json

# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------
st.set_page_config(
    page_title="StudyPartner — UltraAI",
    page_icon="📚",
    layout="wide"
)

# ---------------------------------------------------------
# BASIC STYLES
# ---------------------------------------------------------
st.markdown(
    """
    <style>
    .main-title {
        font-size: 38px;
        font-weight: 800;
        padding: 6px 0px;
    }
    .subtext {
        font-size: 18px;
        opacity: 0.8;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------------------------------------------------
# TITLE
# ---------------------------------------------------------
st.markdown('<div class="main-title">📚 StudyPartner — UltraAI</div>', unsafe_allow_html=True)
st.markdown('<div class="subtext">Your friendly multi-language AI learning partner.</div>', unsafe_allow_html=True)

st.write("---")

# ---------------------------------------------------------
# DATA FOLDER SETUP
# ---------------------------------------------------------
data_dir = Path("user_data")
data_dir.mkdir(exist_ok=True)

# Profile setup
profile_path = data_dir / "profile.json"
default_profile = {
    "name": "Student",
    "age": "",
    "class": "",
    "avatar": "default"
}

if not profile_path.exists():
    profile_path.write_text(json.dumps(default_profile, indent=2))

# ---------------------------------------------------------
# MAIN CONTENT
# ---------------------------------------------------------
st.header("Welcome!")

st.write(
    """
    Use the **sidebar menu** to navigate between:

    - Foundations (LKG–UKG)
    - CBSE Primary (Class 1–5)
    - Tools (Flashcards, Writing, Quizzes)
    - Profile
    - Settings
    """
)

st.subheader("Quick Navigation")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🧸 Foundations"):
        st.query_params["page"] = "2_foundations"
        st.rerun()

with col2:
    if st.button("📘 CBSE Primary"):
        st.query_params["page"] = "3_cbse_primary"
        st.rerun()

with col3:
    if st.button("🧰 Tools"):
        st.query_params["page"] = "4_tools"
        st.rerun()

st.write("---")

st.info("Tip: All lesson pages are inside the **pages/** folder. Streamlit loads them automatically.")

# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------
st.caption("Made with ❤️ for students in India — NCERT aligned")

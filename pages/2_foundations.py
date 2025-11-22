import streamlit as st

st.set_page_config(page_title="Foundations — StudyPartner")

st.title("🧸 Foundations (LKG–UKG)")
st.write("Choose a learning category:")

categories = [
    ("Alphabet & Phonics", "alphabet"),
    ("Numbers 1–20", "numbers"),
    ("Shapes", "shapes"),
    ("Colours", "colors"),
    ("Fruits", "fruits"),
    ("Animals", "animals"),
    ("Environment", "environment"),
    ("Basic Awareness", "awareness"),
]

cols = st.columns(2)

for i, (label, page_name) in enumerate(categories):
    with cols[i % 2]:
        if st.button(label, key=f"btn_{i}"):
            st.query_params["page"] = f"foundations/{page_name}"
            st.rerun()

st.write("---")
st.info("Foundational Learning based on NCERT FLN norms.")

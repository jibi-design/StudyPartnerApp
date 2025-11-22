import streamlit as st

st.set_page_config(page_title="Tools — StudyPartner")

st.title("🧰 Tools")

tools = [
    "Flashcards",
    "Writing Practice",
    "Speaking Practice",
    "Spelling Test",
    "Quiz Generator",
    "Worksheet Generator",
    "AI Assistant"
]

st.write("Select a tool:")

for t in tools:
    st.button(t)

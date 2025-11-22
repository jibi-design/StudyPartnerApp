import streamlit as st
import json
from pathlib import Path

st.set_page_config(page_title="Settings — StudyPartner")

st.title("⚙️ Settings")

data_path = Path("user_data/settings.json")

defaults = {
    "language": "English",
    "voice": "UK English",
    "theme": "light",
    "font_size": "medium"
}

if data_path.exists():
    settings = json.loads(data_path.read_text())
else:
    settings = defaults
    data_path.write_text(json.dumps(defaults, indent=2))

language = st.selectbox("Language", ["English", "Hindi", "Malayalam"])
voice = st.selectbox("Voice", ["UK English", "Hindi", "Malayalam"])
theme = st.radio("Theme", ["light", "dark", "children"])
font = st.selectbox("Font Size", ["small", "medium", "large"])

if st.button("Save Settings"):
    new_settings = {
        "language": language,
        "voice": voice,
        "theme": theme,
        "font_size": font
    }
    data_path.write_text(json.dumps(new_settings, indent=2))
    st.success("Settings saved!")

import streamlit as st
import json
from pathlib import Path

st.set_page_config(page_title="Profile — StudyPartner")

st.title("👤 Profile")

data_path = Path("user_data/profile.json")

# Load existing profile or create if missing
if data_path.exists():
    try:
        profile = json.loads(data_path.read_text())
    except:
        profile = {}
else:
    profile = {}

# Ensure all required fields exist
defaults = {
    "name": "Student",
    "age": "",
    "class": "",
    "avatar": "default"
}

for key, value in defaults.items():
    if key not in profile:
        profile[key] = value

# === INPUT FIELDS ===
name = st.text_input("Name", profile.get("name", ""))
age = st.text_input("Age", profile.get("age", ""))
grade = st.text_input("Class", profile.get("class", ""))
avatar = st.selectbox("Avatar", ["default", "cartoon_teacher", "robot"], index=0)

if st.button("Save"):
    profile["name"] = name
    profile["age"] = age
    profile["class"] = grade
    profile["avatar"] = avatar

    data_path.write_text(json.dumps(profile, indent=2))
    st.success("Profile updated successfully!")

import streamlit as st

st.set_page_config(page_title="Lesson Video Test")

st.title("🎬 Lesson Video — Sample")

st.write("This is how real AI-generated videos will appear inside StudyPartner.")

# Path of your real video (replace with the real MP4 filename)
video_path = "videos/lesson1_real_video.mp4"

try:
    st.video(video_path)
except:
    st.error("Video not found. Make sure the MP4 file is inside the videos/ folder.")

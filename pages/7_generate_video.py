# pages/7_generate_video.py
import streamlit as st
from pathlib import Path
from ai_video_generator import generate_ai_video

st.set_page_config(page_title="AI Video Generator — Pro", layout="wide")
st.title("🎬 Generate Professional Lesson Video (Option D)")

prompt = st.text_area("Lesson topic (e.g., 'Alphabet A — A for Apple')", height=140)
filename = st.text_input("Optional filename (without extension)")
col1, col2 = st.columns([1,1])
with col1:
    duration = st.number_input("Duration (seconds)", min_value=6, max_value=300, value=30)
    template = st.selectbox("Template", ["clean","kids","dark","gradient"])
with col2:
    voice = st.selectbox("Voice", ["gtts","sapi"])

uploaded = st.file_uploader("Optional images to include (max 4)", accept_multiple_files=True, type=['png','jpg','jpeg'])
assets = None
if uploaded:
    tmp = Path("tmp_assets")
    tmp.mkdir(exist_ok=True)
    assets = []
    for i, f in enumerate(uploaded[:4]):
        p = tmp / f.name
        with open(p, "wb") as out:
            out.write(f.getbuffer())
        assets.append(p)

if st.button("Generate Professional MP4"):
    if not prompt.strip():
        st.error("Please enter a prompt/topic.")
    else:
        with st.spinner("Rendering professional MP4 — this may take 10–90s depending on machine..."):
            try:
                mp4_path, audio_path = generate_ai_video(prompt=prompt, filename=(filename or None), duration=duration, template=template, assets=assets, voice=voice)
                st.success("Video generated:")
                st.video(str(mp4_path))
                if audio_path:
                    st.audio(str(audio_path))
            except Exception as e:
                st.exception(e)

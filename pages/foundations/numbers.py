# pages/foundation_numbers.py
import streamlit as st
from pathlib import Path
import json, time

USER_DATA = Path("user_data")
USER_DATA.mkdir(exist_ok=True)
PROG = USER_DATA / "progress.json"
if not PROG.exists():
    PROG.write_text(json.dumps({"lessons": {}}), encoding="utf-8")

def load_prog():
    try:
        return json.loads(PROG.read_text(encoding="utf-8"))
    except Exception:
        return {"lessons": {}}

def save_prog(p):
    PROG.write_text(json.dumps(p, indent=2), encoding="utf-8")

def render_number_block(n):
    st.subheader(f"Number: {n}")
    st.write("Count the objects and trace on paper.")
    st.markdown(f"<div style='font-size:28px'>{'🔵 ' * n}</div>", unsafe_allow_html=True)

def render():
    st.title("🔢 Numbers & Basics")
    st.markdown("Practice counting 1–20 and basic shapes.")
    n = st.slider("Pick a number to practice", 1, 20, 5)
    render_number_block(n)
    if st.button("I practiced — save progress"):
        p = load_prog()
        p["lessons"][f"number_{n}"] = {"practiced": True, "ts": int(time.time())}
        save_prog(p)
        st.success("Saved.")
    st.markdown("---")
    st.info("Shapes & colours section can be added similarly.")

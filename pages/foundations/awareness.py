# pages/foundation_awareness.py
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

def render():
    st.title("🌍 General Awareness")
    topic = st.selectbox("Topic", ["Animals", "Fruits", "Vegetables", "Family", "Body Parts"])
    data = {
        "Animals": ["Dog", "Cat", "Cow", "Elephant", "Monkey"],
        "Fruits": ["Apple", "Banana", "Mango", "Orange"],
        "Vegetables": ["Carrot", "Potato", "Tomato"],
        "Family": ["Father", "Mother", "Brother", "Sister"],
        "Body Parts": ["Eye", "Ear", "Nose", "Hand", "Leg"]
    }
    st.markdown("### Items")
    for it in data[topic]:
        st.write("•", it)
    if st.button("Mark topic done"):
        p = load_prog()
        p["lessons"][f"awareness_{topic.lower().replace(' ','_')}"] = {"done": True, "ts": int(time.time())}
        save_prog(p)
        st.success("Saved progress.")

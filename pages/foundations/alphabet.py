# pages/foundation_alphabet.py
import streamlit as st
from pathlib import Path
import json, time

USER_DATA = Path("user_data")
USER_DATA.mkdir(exist_ok=True)
PROG = USER_DATA / "progress.json"
if not PROG.exists():
    PROG.write_text(json.dumps({"lessons": {}}), encoding="utf-8")

LETTERS = [
 ("A","Apple, Ant, Airplane"),
 ("B","Ball, Bat"),
 ("C","Cat, Cup"),
 ("D","Dog, Drum"),
 ("E","Elephant, Egg"),
 ("F","Fish, Fan"),
 ("G","Goat, Gate"),
 ("H","Hat, House"),
 ("I","Ice, Ink"),
 ("J","Jam, Jug"),
 ("K","Kite, Key"),
 ("L","Lion, Lamp"),
 ("M","Moon, Mango"),
 ("N","Net, Nest"),
 ("O","Orange, Owl"),
 ("P","Pen, Parrot"),
 ("Q","Queen, Quilt"),
 ("R","Rat, Rainbow"),
 ("S","Sun, Snake"),
 ("T","Tree, Tomato"),
 ("U","Umbrella, Up"),
 ("V","Van, Vase"),
 ("W","Window, Water"),
 ("X","Box, Xylophone"),
 ("Y","Yarn, Yak"),
 ("Z","Zebra, Zip")
]

def load_progress():
    try:
        return json.loads(PROG.read_text(encoding="utf-8"))
    except Exception:
        return {"lessons": {}}

def save_progress(p):
    PROG.write_text(json.dumps(p, indent=2), encoding="utf-8")

def render_letter_ui(letter_tuple):
    letter, examples = letter_tuple
    st.header(f"Letter — {letter}")
    st.write(f"Examples: {examples}")
    st.write("Activity: Trace on paper, say the letter aloud, find objects that start with the letter.")
    st.markdown("### Mini Quiz")
    q = st.radio("Which word starts with this letter?", [examples.split(",")[0], "Ball", "Cat"], key=f"q_{letter}")
    if st.button("Submit Answer", key=f"submit_{letter}"):
        score = 1 if q == examples.split(",")[0] else 0
        st.success(f"Score: {score}/1")
        p = load_progress()
        p["lessons"][f"letter_{letter}"] = {"score": score, "ts": int(time.time())}
        save_progress(p)
        st.info("Progress saved locally.")

def render():
    st.title("🔤 Alphabet & Phonics (A–Z)")
    st.markdown("Choose a letter to practice.")
    letters = [l[0] for l in LETTERS]
    sel = st.selectbox("Letter", letters, index=0)
    # find tuple
    for t in LETTERS:
        if t[0] == sel:
            render_letter_ui(t)
            break
    st.markdown("---")
    st.info("I can auto-generate individual A–Z pages on request. This single page handles all letters for speed.")
import streamlit as st
from pathlib import Path

def render():
    st.title("🔤 Alphabet Video Lessons")

    video_path = Path("videos/letter_A.mp4")
    if video_path.exists():
        st.video(str(video_path))
    else:
        st.warning("Video not available. Please add videos/letter_A.mp4")
import streamlit as st

st.title("🔤 Alphabet & Phonics")

st.subheader("AI Teacher")
st.info("Hello! I am your cartoon teacher. Let's learn the alphabet together!")

st.subheader("Flashcards")
cols = st.columns(4)
alphabet = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

for i, letter in enumerate(alphabet):
    with cols[i % 4]:
        st.button(letter)

st.subheader("Mini Quiz")
answer = st.text_input("Type the first letter of 'Apple':")

if answer.lower() == "a":
    st.success("Correct! Great job!")

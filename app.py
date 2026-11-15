import os
import streamlit as st

st.set_page_config(page_title="Open When", page_icon="✉️", layout="centered")

# ------------------------------------------------------------------
# SETTINGS: edit this part
# ------------------------------------------------------------------
HER_NAME = "Adele"     # her name
YOUR_NAME = "Sherzod"     # your name
PASSWORD = "0620"             # e.g. "1409". Leave empty for no password

# Each letter:
#   images: list of image files, e.g. ["images/miss1.jpg"]
#   video : YouTube link or a file, e.g. "https://youtu.be/xxxx" or "videos/hello.mp4"
#   audio : audio file, e.g. "audio/voice.mp3"
# Leave empty if not needed: images=[], video=None, audio=None
LETTERS = [
    {
        "title": "Open when you're sad",
        "text": "I know things feel heavy right now. But remember, you are stronger than "
                "you think, and I am always on your side. Take a deep breath. "
                "This will pass, and I'll be here when it does.",
        "images": ["images/sad1.jpg"],
        "video": None,
        "audio": None,
    },
    {
        "title": "Open when you miss me",
        "text": "I miss you too. Look at this picture and smile. "
                "We'll see each other soon, and until then, you are always on my mind.",
        "images": ["images/miss1.jpg"],
        "video": None,
        "audio": None,
    },
    {
        "title": "Open when you're angry",
        "text": "Take a moment. Count to ten, drink some water. "
                "If I'm the reason, I'm sorry. Let's talk when you're ready. "
                "You matter more to me than being right.",
        "images": [],
        "video": None,
        "audio": None,
    },
    {
        "title": "Open when you can't sleep",
        "text": "Close your eyes and slow your breathing. Whatever is on your mind "
                "can wait until tomorrow. Goodnight, and sleep well.",
        "images": ["images/goodnight.jpg"],
        "video": None,
        "audio": None,
    },
    {
        "title": "Open when you need a hug",
        "text": "Consider this a long, warm hug from me. "
                "I'll give you a real one as soon as I can.",
        "images": [],
        "video": None,
        "audio": None,
    },
]

# ------------------------------------------------------------------
# DESIGN
# ------------------------------------------------------------------
st.markdown(
    """
    <style>
    .stApp { background: #f6f1ec; }
    .block-container { max-width: 680px; padding-top: 3rem; }

    .page-title {
        text-align: center; font-family: Georgia, serif; font-size: 2rem;
        color: #3b2f2f; margin-bottom: 0.2rem; letter-spacing: 0.5px;
    }
    .page-sub {
        text-align: center; color: #7a6a6a; font-size: 0.98rem; margin-bottom: 2rem;
    }

    div.stButton > button {
        width: 100%; min-height: 64px; border-radius: 8px;
        background: #ffffff; color: #3b2f2f; border: 1px solid #d9cfc7;
        font-size: 0.98rem; font-weight: 500; box-shadow: none; transition: all .15s ease;
    }
    div.stButton > button:hover {
        border-color: #a8524f; color: #a8524f; background: #fffdfb;
    }
    div.stButton > button:focus { box-shadow: none; outline: none; }

    .letter {
        background: #fffdf9; border: 1px solid #e3d9d0; border-radius: 8px;
        padding: 28px 30px; margin: 24px 0 14px 0;
        font-family: Georgia, serif; color: #3b2f2f;
    }
    .letter h3 {
        margin: 0 0 14px 0; font-size: 1.25rem; font-weight: 600; color: #a8524f;
    }
    .letter p { font-size: 1.08rem; line-height: 1.75; margin: 0; color: #3b2f2f; }
    .letter .sign { text-align: right; font-style: italic; margin-top: 18px; color: #7a6a6a; }

    .footer { text-align: center; color: #9a8c8c; font-size: 0.85rem; margin-top: 2.5rem; }
    #MainMenu, footer, header { visibility: hidden; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ------------------------------------------------------------------
# HELPERS
# ------------------------------------------------------------------
def is_url(s: str) -> bool:
    return s.startswith("http://") or s.startswith("https://")


def show_media(letter: dict):
    imgs = letter.get("images") or []
    if isinstance(imgs, str):
        imgs = [imgs]
    for img in imgs:
        if is_url(img) or os.path.exists(img):
            st.image(img, use_container_width=True)
        else:
            st.warning(f"Image not found: {img}")

    video = letter.get("video")
    if video:
        if is_url(video) or os.path.exists(video):
            st.video(video)
        else:
            st.warning(f"Video not found: {video}")

    audio = letter.get("audio")
    if audio:
        if is_url(audio) or os.path.exists(audio):
            st.audio(audio)
        else:
            st.warning(f"Audio not found: {audio}")


# ------------------------------------------------------------------
# PASSWORD (optional)
# ------------------------------------------------------------------
if PASSWORD:
    if not st.session_state.get("auth"):
        st.markdown('<p class="page-title">Private page</p>', unsafe_allow_html=True)
        st.markdown('<p class="page-sub">Please enter the password.</p>', unsafe_allow_html=True)
        pw = st.text_input("Password", type="password", label_visibility="collapsed")
        if pw:
            if pw == PASSWORD:
                st.session_state["auth"] = True
                st.rerun()
            else:
                st.error("Incorrect password.")
        st.stop()

# ------------------------------------------------------------------
# MAIN PAGE
# ------------------------------------------------------------------
st.markdown('<p class="page-title">Open When</p>', unsafe_allow_html=True)
st.markdown(
    f'<p class="page-sub">{HER_NAME}, these letters are for you. Open one whenever you need it.</p>',
    unsafe_allow_html=True,
)

if "open_idx" not in st.session_state:
    st.session_state.open_idx = None

cols = st.columns(2)
for i, letter in enumerate(LETTERS):
    with cols[i % 2]:
        if st.button(letter["title"], key=f"btn_{i}", use_container_width=True):
            st.session_state.open_idx = i

idx = st.session_state.open_idx
if idx is not None:
    L = LETTERS[idx]
    st.markdown(
        f"""
        <div class="letter">
            <h3>{L['title']}</h3>
            <p>{L['text']}</p>
            <p class="sign">Yours, {YOUR_NAME}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    show_media(L)
    if st.button("Close", key="close"):
        st.session_state.open_idx = None
        st.rerun()

st.markdown('<p class="footer">Made with love.</p>', unsafe_allow_html=True)

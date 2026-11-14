import os
import streamlit as st

st.set_page_config(page_title="Open When... 💌", page_icon="💌", layout="centered")

# ------------------------------------------------------------------
# ⚙️ SOZLAMALAR — shu qismni o'zingizga moslab o'zgartiring
# ------------------------------------------------------------------
HER_NAME = "Adele"           # uning ismi
YOUR_NAME = "Sherzod"  # sizning ismingiz
PASSWORD = "0620"                   # masalan "1409". Bo'sh qoldirsangiz parol so'ralmaydi

# Har bir xat:
#   images: rasmlar ro'yxati  -> ["sad1, miss1, goodnigh"]
#   video : YouTube havola YOKI fayl -> "https://youtu.be/xxxx" yoki "videos/hello.mp4"
#   audio : ovozli xabar/qo'shiq fayli -> "audio/voice.mp3"
# Keraksiz bo'lsa: images=[], video=None, audio=None
LETTERS = [
    {
        "title": "Open when you're sad",
        "emoji": "🥺",
        "text": "Bilaman, hozir qiyin. Lekin esingda tut: sen juda kuchlisan va men doim yoningdaman. "
                "Chuqur nafas ol, bu kunlar ham o'tib ketadi. Seni qattiq yaxshi ko'raman. ❤️",
        "images": ["images/sad1.jpg"],
        "video": None,
        "audio": None,
    },
    {
        "title": "Open when you miss me",
        "emoji": "🥰",
        "text": "Men ham seni sog'inyapman! Mana bizning rasmimiz, qarab tabassum qil. "
                "Tez orada ko'rishamiz. 💕",
        "images": ["images/miss1.jpg"],   # masalan ["images/miss1.jpg", "images/miss2.jpg"]
        "video": None,
        "audio": None,
    },
    {
        "title": "Open when you're angry",
        "emoji": "😤",
        "text": "Avval 10 gacha sana. Keyin bir stakan suv ich. Agar mendan xafa bo'lsang, "
                "kechir, gaplashib hal qilamiz. Sen uchun doim vaqtim bor. 🌷",
        "images": [],
        "video": None,
        "audio": None,
    },
    {
        "title": "Open when you can't sleep",
        "emoji": "🌙",
        "text": "Ko'zingni yum va men seni mahkam quchoqlab turganimni tasavvur qil. ",
        "images": ["images/goodnight.jpg"],
        "video": None,
        "audio": None,   # masalan "audio/goodnight.mp3"
    },
    {
        "title": "Open when you need a hug",
        "emoji": "🤗",
        "text": "Hozircha yostiqni quchoqlab tur! 🫂 Yaqinda real hayotda seni quchoqlab olaman, va'da beraman.",
        "images": [],
        "video": None,
        "audio": None,
    },
]

# ------------------------------------------------------------------
# 🎨 DIZAYN
# ------------------------------------------------------------------
st.markdown(
    """
    <style>
    .stApp { background: linear-gradient(160deg, #ffd6e0 0%, #ffb3c6 50%, #f8a5c2 100%); }
    h1, h2, h3, p, label, .stMarkdown { color: #5a1a35 !important; }
    .title { text-align:center; font-size: 2.4rem; font-weight: 800; margin-bottom: 0; }
    .sub { text-align:center; opacity:.85; margin-bottom: 1.5rem; }
    div.stButton > button {
        width: 100%; height: 90px; border-radius: 18px; border: 2px solid #fff;
        background: #fff7f9; color: #b0124a; font-size: 1.05rem; font-weight: 700;
        box-shadow: 0 6px 16px rgba(176,18,74,.25); transition: all .2s ease;
    }
    div.stButton > button:hover { transform: translateY(-4px) scale(1.02); background:#fff; border-color:#e63977; color:#e63977; }
    .letter {
        background: #fffaf5; border-radius: 16px; padding: 26px 28px; margin-top: 18px; margin-bottom: 14px;
        border: 2px dashed #e63977; box-shadow: 0 10px 24px rgba(0,0,0,.12);
        font-family: Georgia, serif; font-size: 1.15rem; line-height: 1.7; color: #4a2030;
    }
    .letter h3 { color: #b0124a !important; margin-top: 0; }
    .sign { text-align: right; font-style: italic; margin-top: 14px; color:#b0124a; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ------------------------------------------------------------------
# 🧩 YORDAMCHI: media ko'rsatish
# ------------------------------------------------------------------
def is_url(s: str) -> bool:
    return s.startswith("http://") or s.startswith("https://")


def show_media(L: dict):
    # Rasmlar
    imgs = L.get("images") or []
    if isinstance(imgs, str):
        imgs = [imgs]
    for img in imgs:
        if is_url(img) or os.path.exists(img):
            st.image(img, use_container_width=True)
        else:
            st.warning(f"Rasm topilmadi: {img}")

    # Video (YouTube havola yoki mp4 fayl)
    video = L.get("video")
    if video:
        if is_url(video) or os.path.exists(video):
            st.video(video)
        else:
            st.warning(f"Video topilmadi: {video}")

    # Audio (mp3 / wav / m4a)
    audio = L.get("audio")
    if audio:
        if is_url(audio) or os.path.exists(audio):
            st.audio(audio)
        else:
            st.warning(f"Audio topilmadi: {audio}")


# ------------------------------------------------------------------
# 🔒 PAROL (ixtiyoriy)
# ------------------------------------------------------------------
if PASSWORD:
    if not st.session_state.get("auth"):
        st.markdown('<p class="title">🔒 Maxfiy sahifa</p>', unsafe_allow_html=True)
        pw = st.text_input("Parolni kiriting (bizning maxsus sanamiz 😉)", type="password")
        if pw:
            if pw == PASSWORD:
                st.session_state["auth"] = True
                st.rerun()
            else:
                st.error("Noto'g'ri parol, yana urinib ko'r 💔")
        st.stop()

# ------------------------------------------------------------------
# 💌 ASOSIY SAHIFA
# ------------------------------------------------------------------
st.markdown('<p class="title">💌 Open When...</p>', unsafe_allow_html=True)
st.markdown(
    f'<p class="sub">{HER_NAME}, sen uchun maxsus xatlar. Kerakli paytda konvertni och! 💗</p>',
    unsafe_allow_html=True,
)

if "open_idx" not in st.session_state:
    st.session_state.open_idx = None

cols = st.columns(2)
for i, letter in enumerate(LETTERS):
    with cols[i % 2]:
        if st.button(f"{letter['emoji']}  {letter['title']}", key=f"btn_{i}"):
            st.session_state.open_idx = i
            st.balloons()

idx = st.session_state.open_idx
if idx is not None:
    L = LETTERS[idx]
    st.markdown(
        f"""
        <div class="letter">
            <h3>{L['emoji']} {L['title']}</h3>
            <p>{L['text']}</p>
            <p class="sign">— {YOUR_NAME} ❤️</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    show_media(L)
    if st.button("✖ Yopish", key="close"):
        st.session_state.open_idx = None
        st.rerun()

st.markdown("<br><p style='text-align:center'>Seni sevaman 💖</p>", unsafe_allow_html=True)

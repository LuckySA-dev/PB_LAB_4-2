import streamlit as st
import os
import streamlit.components.v1 as components

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Music Playlist App", layout="wide")

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ---------------- SESSION STATE ----------------
if "playlist" not in st.session_state:
    st.session_state.playlist = []

if "current_index" not in st.session_state:
    st.session_state.current_index = 0

# ---------------- HELPER : ALERT ----------------
def show_alert(message):
    components.html(
        f"""
        <script>
            alert("{message}");
        </script>
        """,
        height=0,
    )

# ---------------- SIDEBAR : ADD SONG ----------------
st.sidebar.title("Add New Song")

title = st.sidebar.text_input("Title")
artist = st.sidebar.text_input("Artist")
uploaded_file = st.sidebar.file_uploader(
    "Upload Audio File (.mp3 / .wav)",
    type=["mp3", "wav"]
)

if st.sidebar.button("Add Song to Playlist"):
    if uploaded_file and title and artist:
        path = os.path.join(UPLOAD_DIR, uploaded_file.name)
        with open(path, "wb") as f:
            f.write(uploaded_file.read())

        st.session_state.playlist.append({
            "title": title,
            "artist": artist,
            "path": path
        })
        st.sidebar.success("Song added successfully!")
    else:
        st.sidebar.warning("Please fill all fields and upload a song")

# ---------------- SIDEBAR : DELETE ----------------
st.sidebar.divider()
st.sidebar.title("Delete Song")

delete_title = st.sidebar.text_input("Song Title to Delete")

if st.sidebar.button("Delete Song"):
    before = len(st.session_state.playlist)
    st.session_state.playlist = [
        s for s in st.session_state.playlist if s["title"] != delete_title
    ]
    if len(st.session_state.playlist) < before:
        st.sidebar.success("Song deleted")
        st.session_state.current_index = 0
    else:
        st.sidebar.error("Song not found")

# ---------------- MAIN ----------------
st.title("🎵 Music Playlist App")
st.subheader("Your Current Playlist")

if st.session_state.playlist:
    for i, song in enumerate(st.session_state.playlist, start=1):
        marker = "▶️" if i - 1 == st.session_state.current_index else ""
        st.write(f"{i}. **{song['title']}** - {song['artist']} {marker}")
else:
    st.info("No songs in playlist")

# ---------------- CONTROLS ----------------
st.subheader("Playback Controls")

audio_placeholder = st.empty()

c1, c2, c3 = st.columns(3)

with c1:
    if st.button("⏮ Previous"):
        if st.session_state.current_index > 0:
            st.session_state.current_index -= 1
        else:
            show_alert("Already at the beginning of the playlist.")

with c2:
    st.button("▶ Play Current")

with c3:
    if st.button("⏭ Next"):
        if st.session_state.current_index < len(st.session_state.playlist) - 1:
            st.session_state.current_index += 1
        else:
            show_alert("End of playlist. No next song.")

# ---------------- AUDIO PLAYER ----------------
if st.session_state.playlist:
    song = st.session_state.playlist[st.session_state.current_index]

    st.info(f"Now playing: {song['title']} - {song['artist']}")

    with audio_placeholder:
        st.audio(open(song["path"], "rb").read(), format="audio/mp3")

st.caption(f"Total songs in playlist: {len(st.session_state.playlist)} song(s)")

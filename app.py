import os
import streamlit as st
import yt_dlp as ytd

st.set_page_config(page_title="Audio-Video Downloader")
st.title("Audio-Video Downloader")

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

link = st.text_input("Enter the URL of the audio or video you want to download:")
format_choice = st.selectbox("Select the format", ["mp3", "mp4"])

# ---------- PREVIEW ----------
if st.button("Preview"):
    if not link:
        st.error("Please enter a valid URL")
        st.stop()

    try:
        with ytd.YoutubeDL({"quiet": True}) as ydl:
            info = ydl.extract_info(link, download=False)

        if format_choice == "mp3":
            # best audio-only stream
            audio_formats = [
                f for f in info["formats"]
                if f.get("acodec") != "none"
            ]
            best_audio = max(audio_formats, key=lambda x: x.get("abr", 0))
            st.subheader("Audio Preview")
            st.audio(best_audio["url"])

        else:
            # best progressive video (audio+video)
            video_formats = [
                f for f in info["formats"]
                if f.get("vcodec") != "none" and f.get("acodec") != "none"
            ]
            best_video = max(video_formats, key=lambda x: x.get("height", 0))
            st.subheader("Video Preview")
            st.video(best_video["url"])

    except Exception:
        st.error("Preview not available for this URL.")

st.markdown("---")

# ---------- DOWNLOAD ----------
if st.button("Download"):
    if not link:
        st.error("Please enter a valid URL")
        st.stop()

    try:
        if format_choice == "mp3":
            ydl_opts = {
                "format": "bestaudio/best",
                "outtmpl": f"{DOWNLOAD_DIR}/%(title)s.%(ext)s",
                "postprocessors": [{
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }],
                "quiet": True,
                "noplaylist": True,
            }
        else:
            ydl_opts = {
                "format": "best[ext=mp4]/best",
                "outtmpl": f"{DOWNLOAD_DIR}/%(title)s.%(ext)s",
                "merge_output_format": "mp4",
                "quiet": True,
                "noplaylist": True,
            }

        with ytd.YoutubeDL(ydl_opts) as ydl:
            ydl.download([link])

        st.success("Download completed successfully!")

    except Exception:
        st.error("Download failed.")

import os
import streamlit as st
import yt_dlp as ytd

st.set_page_config(page_title="Audio-Video Downloader")
st.title("Audio-Video Downloader")

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

link = st.text_input("Enter the URL of the audio or video you want to download:")
format_choice = st.selectbox("Select the format", ["mp3", "mp4"])

if st.button("Download"):
    if not link:
        st.error("Please enter a valid URL")
        st.stop()

    try:
        if format_choice == "mp3":
            ydl_opts = {
                'format': 'bestaudio[ext=m4a]/bestaudio/best',
                'outtmpl': f'{DOWNLOAD_DIR}/%(title)s.%(ext)s',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'quiet': True,
                'nocheckcertificate': True,
                'noplaylist': True,
            }
        else:
            ydl_opts = {
                'format': 'best[ext=mp4]/best',
                'outtmpl': f'{DOWNLOAD_DIR}/%(title)s.%(ext)s',
                'merge_output_format': 'mp4',
                'quiet': True,
                'nocheckcertificate': True,
                'noplaylist': True,
            }

        with ytd.YoutubeDL(ydl_opts) as ydl:
            ydl.download([link])

        st.success("Download completed successfully!")

    except Exception:
        st.error("Download failed. This video may be restricted or blocked by YouTube.")

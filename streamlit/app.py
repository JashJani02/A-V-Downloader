import streamlit as st
import yt_dlp as ytd

st.write("# Audio-Video Downloader")

link = st.text_input("Enter the URL of the audio or video you want to download:")

format_choice = st.selectbox("Select the format:- Audio/Video", options=["mp3", "mp4"])

if st.button("Download"):
    if link:
        if format_choice == "mp3":
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'outtmpl': '%(title)s.%(ext)s',
            }

        else:  # MP4
            ydl_opts = {
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',
                'merge_output_format': 'mp4',
                'outtmpl': '%(title)s.%(ext)s',
            }

        with ytd.YoutubeDL(ydl_opts) as ydl:
            ydl.download([link])

        st.success(f"Download completed! File saved as .{format_choice}")
    else:
        st.error("Please enter a valid URL.")

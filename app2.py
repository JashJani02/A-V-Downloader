import streamlit as st
import yt_dlp as ytd
from pytube import YouTube
import tempfile
import os

st.write("# Audio-Video Downloader")

link = st.text_input("Enter the URL of the audio or video you want to download:")

format_choice = st.selectbox(
    "Select the format",
    options=["mp3", "mp4"]
)

if st.button("Download"):
    if not link:
        st.error("Please enter a valid URL.")
    else:
        with st.spinner("Downloading... please wait"):
            try:
                # ---------- yt-dlp (PRIMARY) ----------
                with tempfile.TemporaryDirectory() as temp_dir:
                    outtmpl = os.path.join(temp_dir, "%(title)s.%(ext)s")

                    if format_choice == "mp3":
                        ydl_opts = {
                            "format": "bestaudio/best",
                            "outtmpl": outtmpl,
                            "postprocessors": [{
                                "key": "FFmpegExtractAudio",
                                "preferredcodec": "mp3",
                                "preferredquality": "192",
                            }],
                        }
                    else:
                        ydl_opts = {
                            "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best",
                            "merge_output_format": "mp4",
                            "outtmpl": outtmpl,
                        }

                    with ytd.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(link, download=True)
                        file_path = ydl.prepare_filename(info)

                        if format_choice == "mp3":
                            file_path = os.path.splitext(file_path)[0] + ".mp3"

                st.success("Downloaded using yt-dlp ✅")

            except Exception as ytdlp_error:
                # ---------- pytube (FAIL-SAFE, YOUTUBE ONLY) ----------
                try:
                    if "youtube.com" not in link and "youtu.be" not in link:
                        raise Exception("Fallback only available for YouTube")

                    with tempfile.TemporaryDirectory() as temp_dir:
                        yt = YouTube(link)

                        if format_choice == "mp3":
                            stream = yt.streams.filter(only_audio=True).first()
                            file_path = stream.download(output_path=temp_dir)
                        else:
                            stream = yt.streams.filter(
                                progressive=True,
                                file_extension="mp4"
                            ).order_by("resolution").desc().first()
                            file_path = stream.download(output_path=temp_dir)

                    st.warning("yt-dlp failed, used pytube fallback ⚠️")

                except Exception as pytube_error:
                    st.error("Download failed ❌")
                    st.exception(pytube_error)
                    st.stop()

            # ---------- Serve file to user ----------
            with open(file_path, "rb") as f:
                st.download_button(
                    label="Click here to download your file",
                    data=f,
                    file_name=os.path.basename(file_path),
                    mime="audio/mpeg" if format_choice == "mp3" else "video/mp4"
                )

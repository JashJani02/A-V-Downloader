import os
import streamlit as st
import yt_dlp as ytd

st.set_page_config(page_title="Audio-Video Downloader")
st.title("Audio-Video Downloader")

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def get_video_resolutions(url):
    with ytd.YoutubeDL({"quiet":True}) as ydl:
        info = ydl.extract_info(url=url,download=False)

    if "entries" in info:
        info = info["entries"][0]

    resolutions = set()

    for f in info["formats"]:
        if f.get("vcodec") != "none" and f.get("height"):
            resolutions.add(f["height"])

    return sorted(resolutions)

def get_preview_info(url):
    with ytd.YoutubeDL({"quiet":True}) as ydl:
        info = ydl.extract_info(url=url,download=False)

    if "entries" in info:
        info = info["entries"][0]

    return info

link = st.text_input("Enter the URL of the audio or video you want to download:")
media_type = st.selectbox("Select media type", ["audio", "video"])

audio_formats = None

if media_type == "audio":
    audio_formats = st.selectbox("Select audio format",["mp3","flac","wav"])

resolution = None

if media_type == "video" and link:
    try:
        resolutions = get_video_resolutions(link)

        if resolutions:
            resolution = st.selectbox("Select video resolution",resolutions,index=len(resolutions)-1)

    except:
        pass


# ---------- PREVIEW ----------
if st.button("Preview"):
    if not link:
        st.error("Please enter a valid URL")
        st.stop()

    try:
  
        info = get_preview_info(link)

        st.subheader(info["title"])

        if media_type == "audio":
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

            if resolution:
                video_formats = [
                    f for f in video_formats
                    if f.get("height") == resolution
                ] or video_formats

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
        if media_type == "audio":
            ydl_opts = {
                "format": "bestaudio/best",
                "outtmpl": f"{DOWNLOAD_DIR}/%(playlist_title)s/%(title)s.%(ext)s",

                "postprocessors": [
                    {
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": audio_formats,
                        "preferredquality": "192",
                    },
                    {
                        "key": "EmbedThumbnail"
                    },
                    {
                        "key": "FFmpegMetadata"
                    }
                ],

                "writethumbnail": True,
                "quiet": True,
                "noplaylist": False,
            }
        else:

            if resolution:
                format_string = f"bestvideo[ext=mp4][height<={resolution}]+bestaudio[ext=m4a]/best[ext=mp4]"
            
            else:
                format_string = "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]"

            ydl_opts = {

                "format": format_string,

                "outtmpl": f"{DOWNLOAD_DIR}/%(playlist_title)s/%(title)s.%(ext)s",

                "merge_output_format": "mp4",

                "writesubtitles": True,
                "writeautomaticsub": True,
                "subtitleslangs": ["en"],
                "nooverwrites": True,
                "quiet": True,
                "noplaylist": False,
            }

        with ytd.YoutubeDL(ydl_opts) as ydl:
            ydl.download([link])

        st.success("Download completed successfully!")

    except Exception:
        st.error("Download failed.")

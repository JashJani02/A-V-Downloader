import os
import tempfile
from flask import Flask, render_template, request, send_file
import yt_dlp

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    format_choice = request.form['format']  # video or audio

    # create temp directory
    temp_dir = tempfile.mkdtemp()

    # file output template
    outtmpl = os.path.join(temp_dir, '%(title)s.%(ext)s')

    # base options
    ydl_opts = {
        'outtmpl': outtmpl,
    }

    if format_choice == 'audio':
        ydl_opts.update({
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        })
    else:  # video
        ydl_opts.update({
            'format': 'best[ext=mp4]/best',
        })

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
        if format_choice == 'audio':
            filename = os.path.splitext(filename)[0] + ".mp3"

    return send_file(filename, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
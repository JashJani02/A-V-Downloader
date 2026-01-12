# Audio-Video Downloader

## Python-Libraries used
1). Streamlit.<br>
2). yt_dlp.

### Workflow
1). Enter the url/link for any dersired audio-video<br>
2). Specifically also select the format for the desired format.<br>
3). Click on the "download" button.<br>
4). The backend fetches the url and downloads the audio/video through the yt-dlp library.<br>
5). The file would be downnloaded in the downloads folder of the user's machine.<br>

### Project-setup
<ol>
  <li>Clone the project<br><pre><code>git clone https://github.com/JashJani02/A-V-Downloader.git</code></pre></li>
  <li>Open your Favourite code-editor and intialize a Python Virtual Environment<br><pre><code>python -m venv venv</code></pre></li>
  <li>Activate the Virtual Environment<br><br>1) Windows cmd<br><pre><code>.\<env_name>\Scripts\Activate.ps1</code></pre><br>2) Bash/zsh<br><pre><code>source <env_name>/bin/activate</code></pre></li>
  <li>Download the libraries via the requirements.txt file<br><pre><code>pip install -r requirements.txt</code></pre></li>
  <li>Run the app.py file<br><pre><code>streamlit run app.py</code></pre></li>
</ol>

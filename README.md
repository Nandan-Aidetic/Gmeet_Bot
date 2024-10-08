
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body>

<h1>Google Meet Bot - Auto Join and Record</h1>

<p>This Python project creates an automated bot that joins a Google Meet meeting, records audio, and auto-exits when the host leaves or the bot is the only participant remaining in the meeting. The bot uses <code>undetected-chromedriver</code> for web automation and <code>pyaudio</code> to record the audio stream.</p>

<h2>Features</h2>
<ul>
    <li><strong>Automatic Google Meet Joining</strong>: The bot can join a Google Meet session as a guest.</li>
    <li><strong>Mute Microphone and Camera</strong>: Ensures the bot does not transmit audio or video during the session.</li>
    <li><strong>Audio Recording</strong>: Records audio from the meeting using <code>pyaudio</code>.</li>
</ul>

<h2>Folder Structure</h2>
<pre>
.
├── meet_bot
│   ├── __init__.py
│   ├── audio.py         # Audio recording and noise reduction logic
│   ├── meet.py          # Main logic for joining and managing the Google Meet
│   ├── config.py        # Configuration and utility functions
</pre>

<h2>Requirements</h2>
<p>Make sure you have the following installed:</p>
<ul>
    <li>Python 3.8+</li>
    <li>Google Chrome (or Chromium)</li>
</ul>

<h3>Python Libraries</h3>
<pre>
pip install -r requirements.txt
</pre>
<p>This will install all the necessary Python dependencies, including:</p>
<ul>
    <li><code>undetected-chromedriver</code></li>
    <li><code>selenium</code></li>
    <li><code>pyaudio</code></li>
</ul>

<h2>Usage</h2>

<h3>Step 1: Set Up the Configuration</h3>
<p>Update the <code>meet_bot/config.py</code> file with your Google Meet URL and other necessary configuration settings.</p>

<h3>Step 2: Start the Bot</h3>
<pre>
python3 meet_bot/meet.py
</pre>
<p>This will start the bot, which will automatically join the Google Meet, mute audio and video, and start recording the session. The audio is saved as a WAV file after the session ends.</p>


<h2>License</h2>
<p>This project is licensed under the MIT License. Feel free to modify and distribute as per the terms of the license.</p>

</body>
</html>

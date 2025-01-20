from __future__ import unicode_literals
import yt_dlp
import ffmpeg
import sys
import os

# Ensure the directory exists
output_directory = './Downloaded_WAV'
os.makedirs(output_directory, exist_ok=True)

ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': f'{output_directory}/%(title)s.%(ext)s',  # Save file to the specified directory
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'wav',
    }],
}

def download_from_url(url):
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

args = sys.argv[1:]
if len(args) > 1:
    print("Too many arguments.")
    print("Usage: python youtubetowav.py <optional link>")
    print("If a link is given it will automatically convert it to .wav. Otherwise a prompt will be shown")
    exit()
if len(args) == 0:
    url = input("Enter Youtube URL: ")
    download_from_url(url)
else:
    download_from_url(args[0])

print("Conversion Complete")
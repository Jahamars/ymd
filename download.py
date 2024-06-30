import yt_dlp
import urllib.parse
import requests
import os
import re

def search_and_download(query, output_dir="downloads"):
    search_url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(query)}"
    response = requests.get(search_url)
    video_ids = re.findall(r"watch\?v=(\S{11})", response.text)
    
    if video_ids:
        video_url = f"https://www.youtube.com/watch?v={video_ids[0]}"
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': f'{output_dir}/%(title)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
    else:
        print(f"No results found for: {query}")

output_dir = "downloads"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

with open('sorted_songs.txt', 'r', encoding='utf-8') as file:
    for line in file:
        song = line.strip()
        if song:
            print(f"Downloading: {song}")
            search_and_download(song, output_dir=output_dir)

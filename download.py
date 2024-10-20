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
        
        # Получаем информацию о видео
        ydl_opts_info = {
            'quiet': True,
            'skip_download': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts_info) as ydl:
            info = ydl.extract_info(video_url, download=False)
            video_title = info.get('title', 'unknown').replace('/', '_')  # Убираем символы, которые могут быть недопустимы в именах файлов

        # Проверяем, существует ли уже файл
        file_path = os.path.join(output_dir, f"{video_title}.mp3")
        if os.path.exists(file_path):
            print(f"File already exists: {file_path}")
            return
        
        # Параметры загрузки
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

import re

def extract_songs(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    songs = []
    for i in range(len(lines)):
        line = lines[i].strip()
        if line and not re.match(r'^\d+:\d{2}$', line) and not re.match(r'^\s*$', line):
            next_line = lines[i+1].strip() if i+1 < len(lines) else ""
            if not re.match(r'^\d+:\d{2}$', next_line) and not re.match(r'^\s*$', next_line):
                song = line
                artist = next_line
                songs.append(f"{song} - {artist}")
    
    with open(output_file, 'w', encoding='utf-8') as file:
        for song in songs:
            file.write(song + '\n')

input_file = 'ymusic.txt'
output_file = 'sorted_songs.txt'

extract_songs(input_file, output_file)

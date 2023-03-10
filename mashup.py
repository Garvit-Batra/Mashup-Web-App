import os
import requests
import subprocess
import sys
import zipfile
from pydub import AudioSegment

def downloadSongs(search_query,n,end_time):
    url = 'https://www.youtube.com/results?search_query=' + search_query
    html_content = requests.get(url).text
    video_links = set()
    i=0
    while(1):
        print("downloading songs")
        if(len(video_links)==n):
            break
        video_links.add('https://www.youtube.com/watch?v=' + html_content.split("watch?v=")[i + 1].split("\"")[0])
        i=i+1
    if not os.path.exists('songs'):
        os.makedirs('songs')
    for link in video_links:
        start_time = 0
        subprocess.run(['yt-dlp', link,"--extract-audio","--audio-format", "mp3","--max-filesize", "5m", "-o", f"songs/%(title)s.%(ext)s", "--postprocessor-args", f"-ss {start_time} -t {end_time - start_time}"])

def mergeSongs(output_file):
    print("In merge function")
    folder = "songs"
    audio_files = [f for f in os.listdir(folder) if f.endswith('.mp3')]
    merged_audio = AudioSegment.from_mp3(os.path.join(folder, audio_files[0]))
    for audio_file in audio_files[1:]:
        audio = AudioSegment.from_mp3(os.path.join(folder, audio_file))
        merged_audio = merged_audio + audio
    merged_audio.export(output_file, format="mp3")
    zip_file = "output.zip"
    with zipfile.ZipFile(zip_file, 'w') as myzip:
        myzip.write(output_file)

def main():
    search_query = sys.argv[1]
    n = int(sys.argv[2])
    end_time = int(sys.argv[3])
    output_file = sys.argv[4]
    downloadSongs(search_query,n,end_time)
    mergeSongs(output_file)

if __name__ == "__main__":
    main()
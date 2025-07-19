# ===================================================================================
# Search all videos in a YouTube Channel
# And save search results in csv file
# with 'Video ID', 'Title', 'URL' format
# ===================================================================================
import yt_dlp
import csv
import configparser
import os
# ===================================================================================
# Read from settings.ini
config = configparser.ConfigParser()
config.read('settings.ini')

channel_url = config.get('Settings', 'channel_url')
output_csv = config.get('Settings', 'csv_name')
# ===================================================================================
ydl_opts = {
    'quiet': True,
    'ignoreerrors': True,
    'extract_flat': True,  # get metadata only, not full video details
    'skip_download': True,
    'force_generic_extractor': True  # important: treat /videos page as a generic extractor
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    info = ydl.extract_info(channel_url, download=False)

videos = info.get('entries', []) if info else []
# ===================================================================================
with open(output_csv, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Video ID', 'Title', 'URL'])

    for video in videos:
        if video and 'id' in video and 'title' in video:
            video_id = video['id']
            title = video['title']
            url = f"https://www.youtube.com/watch?v={video_id}"
            writer.writerow([video_id, title, url])
# ===================================================================================
print(f"\n\033[92m[INFO]\033[0m Exported {len(videos)} videos to {output_csv}")

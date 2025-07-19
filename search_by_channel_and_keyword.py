# ===================================================================================
# Search all videos in a YouTube Channel
# Filter by keyword
# Save matched results in CSV file (same folder as script)
# ===================================================================================
import yt_dlp
import csv
import configparser
# ===================================================================================
# Read from settings.ini
config = configparser.ConfigParser()
config.read('settings.ini')

channel_url = config.get('Settings', 'channel_url')
output_csv = config.get('Settings', 'csv_name')
search_keyword = config.get('Settings', 'keyword').lower()  # lowercase for case-insensitive match
# ===================================================================================
ydl_opts = {
    'quiet': True,
    'ignoreerrors': True,
    'extract_flat': True,  # metadata only
    'skip_download': True,
    'force_generic_extractor': True  # treat /videos as generic page
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    info = ydl.extract_info(channel_url, download=False)

videos = info.get('entries', []) if info else []
# ===================================================================================
video_count = 0

with open(output_csv, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Video ID', 'Title', 'URL'])

    for video in videos:
        if video and 'id' in video and 'title' in video:
            title = video['title']
            if search_keyword in title.lower():
                video_id = video['id']
                url = f"https://www.youtube.com/watch?v={video_id}"
                writer.writerow([video_id, title, url])
                video_count += 1
                print(f"\n\033[92m[INFO]\033[0m {video_count} video(s) found.")
                print(f"\033[92m[INFO]\033[0m {title} - added.")
# ===================================================================================
print(f"\n\033[92m[INFO]\033[0m Exported {video_count} videos matching '{search_keyword}' to {output_csv}")

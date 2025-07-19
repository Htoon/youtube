# ===================================================================================
# Download all videos in a YouTube Channel
# After a video was downloaded, pause for 5s to 30s randomly
# Download process will log to a csv file
# ===================================================================================
import yt_dlp
import os
import re
import time
import random
import csv
from datetime import datetime
# ===================================================================================
# Channel and output directory
#channel_url = "https://www.youtube.com/@SlowEasyEnglish/videos"
channel_url = "https://www.youtube.com/@EnglishLingo/videos"
output_dir = "english_lingo_videos"
os.makedirs(output_dir, exist_ok=True)
# ===================================================================================
# Create timestamped log filename
timestamp = datetime.now().strftime("%Y-%m-%d, %H-%M")
log_filename = f"Download Log [{timestamp}].csv"
# Open the CSV file for writing
log_file = open(log_filename, mode='w', newline='', encoding='utf-8')
csv_writer = csv.writer(log_file)
csv_writer.writerow(["Video ID", "Title", "Video Link", "Status"])
# ===================================================================================
# Get list of existing video filenames (lowercased and sanitized)
existing_files = set()
for file in os.listdir(output_dir):
    base_name, _ = os.path.splitext(file)
    existing_files.add(base_name.lower())
# ===================================================================================
# Fetch all videos from the channel (flat list, no download)
print("\033[92m[INFO]\033[0m Fetching video list from the channel...")
ydl_opts_list = {
    'ignoreerrors': True,
    'quiet': True,
    'extract_flat': True,
    'skip_download': True,
}

with yt_dlp.YoutubeDL(ydl_opts_list) as ydl:
    info = ydl.extract_info(channel_url, download=False)

videos = info.get('entries', [])
total_videos = len(videos)
print(f"\033[92m[INFO]\033[0m Total videos found on channel: {total_videos}")
# ===================================================================================
# Set up download options
ydl_opts_download = {
    'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
    'writesubtitles': True,
    'writeautomaticsub': True,
    'subtitleslangs': ['en'],
    'subtitlesformat': 'srt',
    'format': 'bestvideo[height<=720]+bestaudio/best[height<=720]',
    'merge_output_format': 'mp4',
    'quiet': False,
    #'ignoreerrors': True,
}
# ===================================================================================
# Helper: sanitize video titles to match saved filenames
def sanitize_filename(title):
    return re.sub(r'[\\/*?:"<>|]', '', title).strip().lower()
# ===================================================================================
# Download only missing videos
downloaded_count = 0
skip_count = 0
error_count = 0

with yt_dlp.YoutubeDL(ydl_opts_download) as ydl:
	for video in videos:
		if not video or 'id' not in video:
			continue
			
		#print(f"\n\033[92m[INFO]\033[0m \033[94mCurrent Index = {downloaded_count + 1}\033[0m, Total = {total_videos}, \033[93mSkip = {skip_count}\033[0m, \033[91mError = {error_count}\033[0m")
		print(f"\n\033[92m[INFO]\033[0m Current Index = {downloaded_count + 1}, Total = {total_videos}, Skip = {skip_count}, Error = {error_count}")
		title = video.get('title', f"video_{video['id']}")
		sanitized_title = sanitize_filename(title)
		
		video_url = f"https://www.youtube.com/watch?v={video['id']}"
		
		if sanitized_title in existing_files:
			print(f"\033[93m[SKIP]\033[0m Already downloaded: {title}")
			csv_writer.writerow([video['id'], title, video_url, "skipped"])
			skip_count += 1
			continue

		if downloaded_count != 0:
		    # Pause before new video
		    pause = random.randint(5, 30)
		    print(f"\n\033[92m[INFO]\033[0m Pausing {pause}s to avoid rate limits...")
		    for r in range(pause, 0, -1):
			print(f"\r\033[92m[INFO]\033[0m Waiting {r:02d}s", end='', flush=True)
			time.sleep(1)
		    print("\r\033[92m[INFO]\033[0m Pause complete.           ")

		print(f"\033[92m[INFO]\033[0m Downloading: {title} ({video['id']})")
		
		try:
			ydl.download([video_url])
			csv_writer.writerow([video['id'], title, video_url, "succeeded"])
			downloaded_count += 1
			print(f"\033[92m[INFO]\033[0m {downloaded_count} download{'s' if downloaded_count != 1 else ''} complete.")
		except Exception as e:
			print(f"\033[91m[ERROR]\033[0m Failed to download: {title} ({video['id']})")
			print(f"\033[91m[ERROR]\033[0m Reason: {e}")
			csv_writer.writerow([video['id'], title, video_url, "failed"])
			error_count += 1
			continue  # skip to the next video
# ===================================================================================
log_file.close()
print(f"\n\033[92m[INFO]\033[0m Log written to {log_filename}")
print(f"\n\033[92m[INFO]\033[0m Done! Downloaded {downloaded_count} videos.")
print(f"\033[92m[INFO]\033[0m Total = {total_videos}, Download = {downloaded_count}, Skip = {skip_count}, Error = {error_count}")

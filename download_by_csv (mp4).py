# ===================================================================================
# Download all videos in a csv file saved from YouTube
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
# ============================================================================
input_csv = "EnglishLearningHubOfficial.csv"
output_dir = "EnglishLearningHubOfficial"
os.makedirs(output_dir, exist_ok=True)

search_keyword = "grade-10"
# ============================================================================
# Create timestamped log
timestamp = datetime.now().strftime("%Y-%m-%d, %H-%M")
log_filename = f"Download Log [{timestamp}].csv"
log_file = open(log_filename, mode='w', newline='', encoding='utf-8')
csv_writer = csv.writer(log_file)
csv_writer.writerow(["Video ID", "Title", "Video Link", "Status"])
# ============================================================================
# Get list of already-downloaded (sanitized) file names
existing_files = set()
for file in os.listdir(output_dir):
    base_name, _ = os.path.splitext(file)
    existing_files.add(base_name.lower())
# ============================================================================
# Sanitize function for safe file names
def sanitize_filename(name):
    return re.sub(r'[\\/*?:"<>|]', '', name).strip().lower()
# ============================================================================
# Load CSV input (Video ID, Title, URL)
videos = []
with open(input_csv, mode='r', encoding='utf-8') as f:
    reader = csv.reader(f)
    next(reader)  # Skip header
    for row in reader:
        if len(row) >= 3:
            video_id, title, url = row[0], row[1], row[2]
            #if search_keyword in title.lower():  # case-insensitive match
            videos.append((video_id, title, url))

total_videos = len(videos)
print(f"\033[92m[INFO]\033[0m Loaded {total_videos} videos from CSV")
# ============================================================================
# yt-dlp download options
ydl_opts_download = {
    'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
    'writesubtitles': True,
    'writeautomaticsub': True,
    'subtitleslangs': ['en'],
    'subtitlesformat': 'srt',
    'format': 'bestvideo[height<=720]+bestaudio/best[height<=720]',
    'merge_output_format': 'mp4',
    'quiet': False,
}
# ============================================================================
# Start downloading
downloaded_count = 0
skip_count = 0
error_count = 0

with yt_dlp.YoutubeDL(ydl_opts_download) as ydl:
    for index, (video_id, title, url) in enumerate(videos, 1):
        sanitized_title = sanitize_filename(title)

        if sanitized_title in existing_files:
            print(f"\033[93m[SKIP]\033[0m Already downloaded: {title}")
            csv_writer.writerow([video_id, title, url, "skipped"])
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
            
        print(f"\n\033[92m[INFO]\033[0m Current Index = {downloaded_count + 1}, Total = {total_videos}, Skip = {skip_count}, Error = {error_count}")
        print(f"\033[92m[INFO]\033[0m Downloading {title} ({video_id})")

        try:
            ydl.download([url])
            csv_writer.writerow([video_id, title, url, "succeeded"])
            downloaded_count += 1
            print(f"\033[92m[INFO]\033[0m {downloaded_count} download{'s' if downloaded_count != 1 else ''} complete.")
        except Exception as e:
            print(f"\033[91m[ERROR]\033[0m Failed: {title} ({video_id})")
            print(f"\033[91m[ERROR]\033[0m Reason: {e}")
            csv_writer.writerow([video_id, title, url, "failed"])
            error_count += 1
            continue
# ============================================================================
log_file.close()
print(f"\n\033[92m[INFO]\033[0m Log saved to {log_filename}")
print(f"\033[92m[INFO]\033[0m Done. Total: {total_videos}, Downloaded: {downloaded_count}, Skipped: {skip_count}, Failed: {error_count}")

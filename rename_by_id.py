# ============================================================================
# Rename downloaded video and subtitle files using video ID and title from CSV
# ============================================================================
import os
import csv
import re
# ============================================================================
videos_folder = "EnglishLearningHubOfficial"
csv_file = "EnglishLearningHubOfficial.csv"
rename_count = 0
# ============================================================================
def sanitize_filename(name):
    return re.sub(r'[\\/*?:"<>|]', '', name).strip()
# ============================================================================
# Load CSV to map video ID → Title
video_titles = {}
if os.path.exists(csv_file):
    with open(csv_file, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            video_id = row["Video ID"].strip()
            title = row["Title"].strip()
            if video_id and title:
                video_titles[video_id] = title
else:
    print(f"File '{csv_file}' not found.")
    

# ============================================================================
# Rename files
for filename in os.listdir(videos_folder):
    filepath = os.path.join(videos_folder, filename)

    # Try to extract the video ID from filename like "#MkpR0cKWCfE"
    match = re.search(r'#([a-zA-Z0-9_-]{11})', filename)
    if not match:
        continue

    video_id = match.group(1)
    if video_id not in video_titles:
        continue

    new_title = sanitize_filename(video_titles[video_id])
    ext = os.path.splitext(filename)[1]  # preserve original extension (.mp4, .srt, etc.)
    new_filename = f"{new_title}{ext}"
    new_filepath = os.path.join(videos_folder, new_filename)

    if os.path.exists(new_filepath):
        print(f"\033[93m[SKIP]\033[0m Already exists: {new_filename}")
        continue

    try:
        os.rename(filepath, new_filepath)
        print(f"\033[92m[RENAME]\033[0m {filename} → {new_filename}")
        rename_count += 1
    except Exception as e:
        print(f"\033[91m[ERROR]\033[0m Could not rename {filename}: {e}")
# ============================================================================
print(f"\n\033[92m[INFO]\033[0m Done! Renamed {rename_count} file(s).")

# ===================================================================================
# Search all videos in a YouTube Channel
# And save search results in csv file
# with 'Video ID', 'Title', 'URL' format
# ===================================================================================
import yt_dlp
import csv
# ===================================================================================
#channel_videos_url = "https://www.youtube.com/@SlowEasyEnglish/videos"
#channel_videos_url = "https://www.youtube.com/@EnglishLingo/videos"
channel_videos_url = "https://www.youtube.com/@WasoLearn/videos"
output_csv = "waso_videos.csv"
search_keyword = "grade 10"       # Keyword must be in small letter
# ===================================================================================
ydl_opts = {
    'quiet': True,
    'ignoreerrors': True,
    'extract_flat': True,  # get metadata only, not full video details
    'skip_download': True,
    'force_generic_extractor': True  # important: treat /videos page as a generic extractor
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    info = ydl.extract_info(channel_videos_url, download=False)

videos = info.get('entries', []) if info else []
# ===================================================================================
video_count = 0

with open(output_csv, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Video ID', 'Title', 'URL'])

    for video in videos:
        if video and 'id' in video and 'title' in video:
            video_id = video['id']
            title = video['title']
            url = f"https://www.youtube.com/watch?v={video_id}"
            if search_keyword in title.lower():  # case-insensitive match
                #if 'chemistry' in title.lower():
                    writer.writerow([video_id, title, url])
                    video_count += 1
                    print(f"\n\033[92m[INFO]\033[0m {video_count} video(s) found.")
                    print(f"\033[92m[INFO]\033[0m {title} - added.")                    
# ===================================================================================
print(f"\n\033[92m[INFO]\033[0m Exported {video_count} videos matching '{search_keyword}' to {output_csv}")

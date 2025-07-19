# ============================================================================
# Generate Subtitle Files using Whisper Library
# Video files must be in video_folder
# ============================================================================
import configparser
import os
import whisper
# ============================================================================
# Read from settings.ini
config = configparser.ConfigParser()
config.read('settings.ini')

video_folder = config.get('Settings', 'video_dir')
# ============================================================================
# Join script_dir and video_folder
script_dir = os.path.dirname(os.path.abspath(__file__))
video_source_folder = os.path.join(script_dir, video_folder)
# ============================================================================
def generate_srt_for_all_mp4s_in_folder():
    if not os.path.isdir(video_source_folder):
        print(f"\033[91m[ERROR]\033[0m Folder not found: {video_source_folder}")
        return

    model = whisper.load_model("base")  # Use "tiny", "small", etc. as needed

    complete_count = 0
    skip_count = 0

    # Loop through video folder
    for file in os.listdir(video_source_folder):
        if file.lower().endswith(".mp4"):
            file_path = os.path.join(video_source_folder, file)
            base_name = os.path.splitext(file)[0]
            srt_file = os.path.join(video_source_folder, base_name + ".srt")

            if os.path.exists(srt_file):
                print(f"\033[93m[SKIP]\033[0m Skipping {file} (subtitle already exists)")
                skip_count += 1
                continue

            print(f"\n\033[92m[INFO]\033[0m Transcribing: {file}")
            result = model.transcribe(file_path, verbose=True)

            with open(srt_file, "w", encoding="utf-8") as f:
                for i, segment in enumerate(result["segments"], start=1):
                    start = segment["start"]
                    end = segment["end"]
                    text = segment["text"].strip()

                    def format_time(t):
                        h = int(t // 3600)
                        m = int((t % 3600) // 60)
                        s = int(t % 60)
                        ms = int((t - int(t)) * 1000)
                        return f"{h:02}:{m:02}:{s:02},{ms:03}"

                    f.write(f"{i}\n{format_time(start)} --> {format_time(end)}\n{text}\n\n")

            print(f"\033[92m[INFO]\033[0m Subtitle saved: {srt_file}")
            complete_count += 1

    # Final summary split into two lines
    print(f"\n\033[92m[INFO]\033[0m Total {complete_count} file{'s' if complete_count != 1 else ''} generated.")
    print(f"\033[93m[INFO]\033[0m {skip_count} file{'s' if skip_count != 1 else ''} skipped.")
# ============================================================================
if __name__ == "__main__":
    generate_srt_for_all_mp4s_in_folder()

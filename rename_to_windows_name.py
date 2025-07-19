# ============================================================================
# Change file names from Non-Windows Compatible File Names to Windows Compatible Files
# Remove some punctuation characters and Emoji characters
# ============================================================================
import os
import re
# ============================================================================
video_folder = "EnglishLearningHubOfficial"
# ============================================================================
# Sanitize filename
# ============================================================================
def remove_emojis(text):
    return re.sub(r'[\U00010000-\U0010ffff]', '', text)

def sanitize_filename(name: str, replacement="_") -> str:
    name = remove_emojis(name)
    name = re.sub(r'[<>:"/\\|?*]', replacement, name)
    name = name.rstrip('. ')
    return name
# ============================================================================
# Rename files in folder
# ============================================================================
def rename_files_in_folder(folder="."):
    for filename in os.listdir(folder):
        full_path = os.path.join(folder, filename)

        # Skip if not a file
        if not os.path.isfile(full_path):
            continue

        sanitized_name = sanitize_filename(filename)

        # Only rename if needed
        if filename != sanitized_name:
            new_path = os.path.join(folder, sanitized_name)
            print(f"[RENAME] {filename} -> {sanitized_name}")
            os.rename(full_path, new_path)

    print("\n[INFO] All filenames sanitized.")
# ============================================================================
if __name__ == "__main__":
    current_folder = os.path.dirname(os.path.abspath(__file__))
    rename_files_in_folder(f'{current_folder}/{video_folder}')

# ============================================================================
# Change file names from Non-Windows Compatible File Names to Windows Compatible Files
# Remove some punctuation characters and Emoji characters
# ============================================================================
import configparser
import os
import re
# ============================================================================
# Read from settings.ini
config = configparser.ConfigParser()
config.read('settings.ini')

video_folder = config.get('Settings', 'video_dir')
# ============================================================================
# Sanitize filename
def remove_emojis(text):
    # Remove emojis from text (more comprehensive range)
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F1E0-\U0001F1FF"  # flags (iOS)
        "\U00002702-\U000027B0"
        "\U000024C2-\U0001F251"
        "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)

def sanitize_filename(name: str, replacement="_") -> str:
    name = remove_emojis(name)
    # Replace invalid chars for Windows filenames
    name = re.sub(r'[<>:"/\\|?*]', replacement, name)
    # Strip trailing spaces and dots
    name = name.rstrip('. ')
    return name
# ============================================================================
# Rename files in folder with collision handling
def rename_files_in_folder(folder="."):
    existing_names = set(os.listdir(folder))
    
    for filename in os.listdir(folder):
        full_path = os.path.join(folder, filename)

        if not os.path.isfile(full_path):
            continue

        sanitized_name = sanitize_filename(filename)
        if filename == sanitized_name:
            continue

        # Handle collisions by appending a number suffix
        candidate_name = sanitized_name
        name_root, ext = os.path.splitext(sanitized_name)
        counter = 1
        while candidate_name in existing_names:
            candidate_name = f"{name_root}_{counter}{ext}"
            counter += 1

        new_path = os.path.join(folder, candidate_name)
        print(f"[RENAME] {filename} -> {candidate_name}")
        os.rename(full_path, new_path)

        # Update existing_names set
        existing_names.remove(filename)
        existing_names.add(candidate_name)

    print("\n[INFO] All filenames sanitized.")
# ============================================================================
if __name__ == "__main__":
    current_folder = os.path.dirname(os.path.abspath(__file__))
    rename_files_in_folder(os.path.join(current_folder, video_folder))

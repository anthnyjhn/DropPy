import json
from pathlib import Path

CONFIG_FILE = Path(__file__).parent / 'droppy_config.json'

def setup_upload_folder():
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, 'r') as f:
            config = json.load(f)
            return config.get('upload_path')

    print("🗂  First-time setup:")
    default_path = Path.home() / 'MyDropbox'
    use_default = input(f"\nDo you want to create and use '{default_path}' as your upload folder? (Y/n): ").strip().lower()

    if use_default in ('y', '', 'yes'):
        upload_path = default_path
    else:
        while True:
            custom = input("Please enter a valid absolute path to use instead: ").strip()
            upload_path = Path(custom).expanduser()
            if upload_path.is_dir() or not upload_path.exists():
                break
            print("❌ Invalid path. Try again.")

    upload_path.mkdir(parents=True, exist_ok=True)

    with open(CONFIG_FILE, 'w') as f:
        json.dump({'upload_path': str(upload_path)}, f)

    return str(upload_path)

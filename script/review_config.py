import sys
from plutonkit.config import REMOTE_URL_RAW
from plutonkit import __version__

def validate_remote_url_raw():
    version_latest = f"https://raw.githubusercontent.com/fonipts/pluton-lobby/{__version__}/blueprint"
    if REMOTE_URL_RAW != version_latest:
        print("Error: Condition not met in REMOTE_URL_RAW")
        sys.exit(1)
    print("Condition met, continuing...")

validate_remote_url_raw()

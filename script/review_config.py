import sys
from plutonkit.config import REMOTE_URL_RAW

def validate_remote_url_raw():
    if REMOTE_URL_RAW != "https://raw.githubusercontent.com/fonipts/pluton-lobby/main/blueprint":
        print("Error: Condition not met in REMOTE_URL_RAW")
        sys.exit(1)
    print("Condition met, continuing...")

validate_remote_url_raw()

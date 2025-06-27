import os

# Name of the temporary directory
TEMP_DIR = os.path.join(os.path.dirname(__file__), "..", "temp")

def ensure_temp_dir():
    """Ensure the temp directory exists."""
    os.makedirs(TEMP_DIR, exist_ok=True)

def get_temp_path(filename):
    """Return full path for a file in the temp directory."""
    return os.path.abspath(os.path.join(TEMP_DIR, filename))

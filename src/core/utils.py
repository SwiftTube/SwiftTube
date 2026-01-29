import sys
import os
import re

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS

    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def format_visits(visits):
    if visits >= 1_000_000_000_000:
        return f"{visits / 1_000_000_000_000:.1f}T"

    elif visits >= 1_000_000_000:
        return f"{visits / 1_000_000_000:.1f}B"

    elif visits >= 1_000_000:
        return f"{visits / 1_000_000:.1f}M"

    elif visits >= 1_000:
        return f"{visits / 1_000:.1f}K"

    else:
        return str(visits)

def format_bytes(input_bytes):
    units, byte = ['bytes', 'KB', 'MB', 'GB'], 0

    while input_bytes >= 1024 and byte < len(units)-1:
        input_bytes /= 1024
        byte += 1

    return f"{input_bytes:.2f} {units[byte]}"

def sanitize_filename(filename):
    return re.sub(r'[<>:"/\\|?*]', '_', filename)

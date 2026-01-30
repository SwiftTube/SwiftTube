import requests

__author__ = "TrollSkull"
__version__ = "0.1.1"
__license__ = "MIT License"

LATEST_RELEASE = "https://api.github.com/repos/SwiftTube/SwiftTube/releases/latest"

def is_there_a_new_release() -> bool:
    response = requests.get(LATEST_RELEASE, timeout = 10)
    response.raise_for_status()

    data = response.json()
    tag_name = data["tag_name"]

    if tag_name != __version__:
        return True
    
    return False

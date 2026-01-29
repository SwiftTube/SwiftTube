from youtubesearchpython import VideosSearch
import pytubefix
import time

def fetch_video_information(url: str):
    yt = pytubefix.YouTube(url)

    filesizes = {}
    qualities = []

    video_streams = (
        yt.streams
        .filter(progressive=True, file_extension="mp4")
        .order_by("resolution")
    )

    for stream in video_streams:
        resolution = stream.resolution
        filesize = stream.filesize or stream.filesize_approx

        if resolution and filesize:
            filesizes[resolution] = filesize
            qualities.append(resolution)

    audio_stream = (
        yt.streams
        .filter(only_audio=True)
        .order_by("abr")
        .desc()
        .first()
    )

    audio_filesize = None
    
    if audio_stream:
        audio_filesize = audio_stream.filesize or audio_stream.filesize_approx

    return {
        "thumbnail_url": yt.thumbnail_url,
        "author": yt.author,
        "title": yt.title,
        "views": yt.views,
        "filesize": filesizes,
        "qualities": qualities,
        "audio": audio_filesize
    }

def search_video_on_yt(user_query = str, limit = 10) -> str:
    search = VideosSearch(query = user_query, limit = limit)
    urls: list = []

    try:
        for i in range(0, limit):
            urls.append(search.result()["result"][i]["link"])

        return urls

    except IndexError:
        time.sleep(0.1)
        raise

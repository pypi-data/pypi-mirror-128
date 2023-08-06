import youtube_transcript_api
from youtube_transcript_api import YouTubeTranscriptApi
from clarku_youtube_crawler.CrawlerObject import _CrawlerObject
import pandas as pd
from configparser import ConfigParser
import json
import os

CONFIG = "config.ini"
config = ConfigParser(allow_no_value=True)
config.read(CONFIG)


class SubtitleCrawler(_CrawlerObject):
    def __init__(self):
        super().__init__()

    def build(self):
        super().__build__("subtitle")

    def _crawl(self, vid):
        try:
            transcript = YouTubeTranscriptApi.get_transcript(vid)
            return transcript
        except:
            return None
        # except youtube_transcript_api._errors.TranscriptsDisabled as td:
        #     return None
        # except youtube_transcript_api._errors.NoTranscriptFound as td:
        #     return None
        # except youtube_transcript_api._errors.NoTranscriptAvailable as td:
        #     return None

    def crawl_csv(self, **kwargs):
        filename = kwargs.get("filename", None)
        header = kwargs.get("video_header", "videoId")
        accepted_ext = [".csv", ".xlsx"]

        ext = ".csv"
        if filename:
            file, ext = os.path.splitext(filename)
            if ext not in accepted_ext:
                raise ValueError(f"{ext} is not an accepted file type")

        if filename is None:
            raise ValueError("Can't find video list to crawl. Specify the video CSV by filename=YOUR_PATH")

        if ext == ".csv":
            df = pd.read_csv(filename)
        else:
            df = pd.read_excel(filename)

        for vid in df[header]:
            if not os.path.exists(self.subtitle_data_dir + vid[1:] + ".json"):
                print(f'Subtitle {vid} crawled')
                transcript = self._crawl(vid[1:])
                if transcript:
                    with open(self.subtitle_data_dir + vid[1:] + ".json", 'w+') as fp:
                        fp.write(json.dumps(transcript) + "\n")

# clarku-youtube-crawler

Clark University YouTube crawler and JSON decoder for YouTube json. Please read documentation in ``DOCS``

Pypi page: "https://pypi.org/project/clarku-youtube-crawler/"

## Installing
To install,

``pip install clarku-youtube-crawler``

The crawler needs multiple other packages to function. 
If missing requirements (I already include all dependencies so it shouldn't happen), download <a href="https://github.com/ClarkUniversity-NiuLab/clarku-youtube-crawler/blob/master/requirements.txt">``requirements.txt`` </a> .
Navigate to the folder where it contains requirements.txt and run 

``pip install -r requirements.txt``


## YouTube API Key
- Go to https://cloud.google.com/, click console, and create a project. Under Credentials, copy the API key.
- In your project folder, create a "DEVELOPER_KEY.txt" file (must be this file name) and paste your API key. 
- You can use multiple API keys by putting them on different lines in DEVELOPER_KEY.txt. 
- The crawler will use up all quotas of one key and try next one, until all quotas are used up.



## Example usage
Case 1: crawl videos by keywords, 
```
# your_script.py
import clarku_youtube_crawler as cu

test = cu.RawCrawler()
test.build()
test.crawl("any_keyword",start_date=14, start_month=12, start_year=2020, day_count=2)
test.merge_to_workfile()
test.crawl_videos_in_list(comment_page_count=1)
test.merge_all(save_to='FINAL_merged_all.json')
```

Case 2: crawl a videos by a list of ids specified by videoId column in an input CSV
```
import clarku_youtube_crawler as cu
test = cu.RawCrawler()
test.build()
test.crawl_videos_in_list(video_list_workfile="video_list.csv", comment_page_count=1, search_key="any_key")
test.merge_all(save_to='all.json')
```

Case 3: Get a list of channels crawled by keywords. I.e. get all videos in channels who have a video in a specific topic.
You need to run case 1 first to generate a raw video JSON file (FINAL_merged_all.json). 
This code will find all unique channels in the video JSON and generate a list of channels. 
Then it will get all videos of all channels.
```
import clarku_youtube_crawler as cu
channel = cu.ChannelCrawler()
channel.build()
channel.setup_channel(filename='FINAL_merged_all.json', subscriber_cutoff=0, keyword="")
channel.crawl()
channel.crawl_videos_in_list(comment_page_count=3) #100 comments per page, 3 page will crawl first 300 comments
channel.merge_all(save_to='file_of_merged_json.json')

```

Case 4: You already have a list of channels. You want to crawl all videos of the channels in the list:
```
import clarku_youtube_crawler as cu

channel = cu.ChannelCrawler()
channel.build()

channel.crawl(filename='channel_list.csv', channel_header="channelId")
channel.crawl_videos_in_list(comment_page_count=3) #100 comments per page, 3 page will crawl first 300 comments
channel.merge_all(save_to='file_of_merged_json.json')
```

To convert the video JSONs to csv:
```
jsonn = cu.JSONDecoder()
jsonn.load_json("FINAL_merged_all.json")
```

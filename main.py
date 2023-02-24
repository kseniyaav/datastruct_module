import os
from googleapiclient.discovery import build

from dotenv import load_dotenv
api_key = 'AIzaSyBf8KYKumDUiXf2SE0d1VTndB41creSfDw'

class Youtube:
    channel_id = "UCByhZ-JEe5OOZSuq0uaXOng"

    def __init__(self, channel_id, channel_name, channel_description, hm_followers, hm_videos, hm_views):
        load_dotenv()
        youtube = build('youtube', 'v3', developerKey=api_key)
        self.channel_id = channel_id
        self.channel_name = channel_name
        self.channel_description = channel_description
        self.hw_followers = hm_followers
        self.hw_videos = hm_videos
        self.hm_views = hm_views
        self.channel_info = youtube.channels().list(id=channel_id, part='snippet,statistics').execute()

    def print_info(self):
        return self.channel_info

if __name__ == "__main__":
    y = Youtube(1, 2, 3, 4, 5, 6)
    print(y.print_info())


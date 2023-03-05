import os
import json

from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('API_KEY')

class Channel:
    def __init__(self, channel_id_arg):
        youtube = self.get_service()
        channel_info = youtube.channels().list(
            id=channel_id_arg, part='snippet,statistics'
        ).execute()
        snippet = channel_info['items'][0]['snippet']
        statistics = channel_info['items'][0]['statistics']

        self._channel_id = channel_id_arg
        self.title = snippet['title']
        self.description = snippet['description']
        self.url = f'https://www.youtube.com/channel/{channel_id_arg}'
        self.subscriber_count = int(statistics['subscriberCount'])
        self.video_count = int(statistics['videoCount'])
        self.view_count = int(statistics['viewCount'])

    @staticmethod
    def get_service():
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube

    @property
    def channel_id(self):
        return self._channel_id

    @channel_id.setter
    def channel_id(self, new_channel_id):
        self._channel_id = new_channel_id
        self.url = f'https://www.youtube.com/channel/{new_channel_id}'

    def print_info(self):
        return self.channel_info

    def to_json(self, filename):
        data = {
            'channel_id': self._channel_id,
            'title': self.title,
            'description': self.description,
            'url': self.url,
            'subscriber_count': self.subscriber_count,
            'video_count': self.video_count,
            'view_count': self.view_count
        }
        with open(filename, 'w') as f:
            json.dump(data, f)

    def __str__(self):
        return f"Youtube-канал: {self.title}"

    def __add__(self, other):
        return self.subscriber_count + other.subscriber_count

    def __gt__(self, other):
        return self.subscriber_count > other.subscriber_count

    def __lt__(self, other):
        return self.subscriber_count < other.subscriber_count

class Video:
    def __init__(self, video_id):
        youtube = self.get_service()
        video_info = youtube.videos().list(
            id=video_id, part='snippet,statistics'
        ).execute()
        snippet = video_info['items'][0]['snippet']
        statistics = video_info['items'][0]['statistics']

        self.video_id = video_id
        self.title = snippet['title']
        self.view_count = int(statistics['viewCount'])
        self.like_count = int(statistics['likeCount'])

    @staticmethod
    def get_service():
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube

    def __str__(self):
        return f"{self.title}"


class PLVideo(Video):
    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id
        self.playlist_title = self.get_playlist_title(playlist_id)

    def get_playlist_title(self, playlist_id):
        youtube = self.get_service()
        playlist_info = youtube.playlists().list(
            id=playlist_id, part='snippet'
        ).execute()
        return playlist_info['items'][0]['snippet']['title']

    def __str__(self):
        return f"{self.title} ({self.playlist_title})"




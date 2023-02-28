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


if __name__ == "__main__":
    vdud = Channel('UCMCgOm8GZkHp8zJ6l7_hIuA')






import os
import json
import datetime
import isodate

from abc import ABC, abstractmethod
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('API_KEY')


class YoutubeAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.service = build('youtube', 'v3', developerKey=api_key)

    def get_video_info(self, video_id):
        video_info = self.service.videos().list(
            part='snippet, statistics',
            id=video_id
        ).execute()
        return video_info

    def get_video_duration(self, video_id):
        video_info = self.service.videos().list(id=video_id, part='contentDetails').execute()
        duration = video_info['items'][0]['contentDetails']['duration']
        return isodate.parse_duration(duration)

    def get_service(self):
        return self.service


class Channel:
    def __init__(self, channel_id_arg):
        youtube = YoutubeAPI(api_key).get_service()
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

    @property
    def channel_id(self):
        return self._channel_id

    @channel_id.setter
    def channel_id(self, new_channel_id):
        self._channel_id = new_channel_id
        self.url = f'https://www.youtube.com/channel/{new_channel_id}'

    def print_info(self):
        pass

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
        youtube = YoutubeAPI(api_key).get_service()
        video_info = youtube.videos().list(
            id=video_id, part='snippet,statistics'
        ).execute()
        if not video_info['items']:
            self.title = None
            self.like_count = None
        else:
            statistics = video_info['items'][0]['statistics']
            self.title = video_info['items'][0]['snippet']['title']
            self.view_count = int(statistics['viewCount'])
            self.duration = YoutubeAPI(api_key).get_video_duration(video_id)
            self.like_count = int(statistics.get('likeCount', 0))

    def __str__(self):
        return f"{self.title}"


class PLVideo(Video):
    def __init__(self, video_id, playlist_id, duration=None, like_count=None):
        super().__init__(video_id)
        self.playlist_id = playlist_id
        self.playlist_title = self.get_playlist_title(playlist_id)

    def get_playlist_title(self, playlist_id):
        youtube = YoutubeAPI(api_key).get_service()
        playlist_info = youtube.playlists().list(
            id=playlist_id, part='snippet'
        ).execute()
        return playlist_info['items'][0]['snippet']['title']

    def __str__(self):
        return f"{self.title} ({self.playlist_title})"


class PlayList:
    def __init__(self, playlist_id):
        youtube = YoutubeAPI(api_key).get_service()
        playlist_info = youtube.playlists().list(
            id=playlist_id, part='snippet'
        ).execute()
        if 'items' in playlist_info and len(playlist_info['items']) > 0:
            self._playlist_id = playlist_id
            self.title = playlist_info['items'][0]['snippet']['title']
            self.url = f"https://www.youtube.com/playlist?list={playlist_id}"
            self._videos = []
        else:
            raise ValueError(f"Playlist with ID {playlist_id} not found")

    def add_video(self, video_id):
        self._videos.append(PLVideo(video_id, self._playlist_id))

    @property
    def total_duration(self):
        total_seconds = sum([video.duration.total_seconds() for video in self._videos])
        return datetime.timedelta(seconds=total_seconds)

    def show_best_video(self):
        if len(self._videos) == 0:
            print("No videos found in playlist")
        else:
            best_video = max(self._videos, key=lambda video: video.like_count)
            return f"https://www.youtube.com/{best_video.video_id}"


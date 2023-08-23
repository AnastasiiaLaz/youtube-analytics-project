import json
import os
from googleapiclient.discovery import build

API_KEY = 'AIzaSyB9owKVw7SBV925QMSK_qUQhArDFejcnec'


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.channel_id = channel_id
        self.title = ''
        self.description = ''
        self.url = ''
        self.subscriber_count = 0
        self.video_count = 0
        self.view_count = 0

        #self.get_channel_info()

    def get_channel_info(self):
        """
        Получает инфу о канале из YouTube API
        """
        youtube = self.get_service()
        channel = youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        if 'items' in channel:
            channel_info = channel['items'][0]
            self.title = channel_info['items'][0]['snippet']['title']
            self.description = channel_info['snippet']['description']
            self.url = channel_info['snippet']['thumbnails']['default']['url']
            self.subscriber_count = channel_info['statistics']['subscriberCount']
            self.video_count = channel_info['statistics']['videoCount']
            self.view_count = channel_info['statistics']['viewCount']

    def __str__(self):
        return f"{self.title} ({self.url})"

    def __add__(self, other):
        return self.subscriber_count + other.subscriber_count

    def __sub__(self, other):
        return self.subscriber_count - other.subscriber_count

    def __lt__(self, other):
        return self.subscriber_count < other.subscriber_count

    def __le__(self, other):
        return self.subscriber_count <= other.subscriber_count

    def __gt__(self, other):
        return self.subscriber_count > other.subscriber_count

    def __ge__(self, other):
        return self.subscriber_count >= other.subscriber_count

    @classmethod
    def get_service(cls):
        """
        класс-метод, возвращающий объект для работы с YouTube API
        """
        api_key: str = os.getenv('API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube

    def to_json(self, filename):
        """
        метод, сохраняющий в файл значения атрибутов экземпляра `Channel`
        """
        channel_data = {
            "channel_id": self.channel_id,
            "title": self.title,
            "description": self.description,
            "url": self.url,
            "subscriber_count": self.subscriber_count,
            "video_count": self.video_count,
            "view_count": self.view_count
        }
        with open(filename, 'w') as json_file:
            return json.dump(channel_data, json_file, indent=4)



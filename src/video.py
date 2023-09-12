import os
from googleapiclient.discovery import build

API_KEY = 'AIzaSyB9owKVw7SBV925QMSK_qUQhArDFejcnec'


class Video:
    def __init__(self, video_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.video_id = video_id
        api_key: str = os.getenv('API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        video = youtube.videos().list(id=self.video_id, part='snippet,statistics').execute()
        if 'items' in video:
            video_info = video['items'][0]
            self.title = video_info['snippet']['title']
            self.url = video_info['snippet']['thumbnails']['default']['url']
            self.view_count = video_info['statistics']['viewCount']
            self.like_count = video_info['statistics']['likeCount']

    @property
    def __repr__(self):
        return f"{self.__class__.__name__}(title='{self.title}', video_url='{self.url}', view_count={self.view_count}, like_count={self.like_count})"

    def __str__(self):
        return f'{self.title}'


class PLVideo(Video):
    def __init__(self, video_id, playlist_id):
        self.playlist_id = playlist_id
        super().__init__(video_id)

    def __str__(self):
        return f'{self.title}'

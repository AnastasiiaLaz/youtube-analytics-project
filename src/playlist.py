import os
from datetime import timedelta
import isodate

from googleapiclient.discovery import build

API_KEY = 'AIzaSyB9owKVw7SBV925QMSK_qUQhArDFejcnec'


class MixinYouTube:

    @classmethod
    def get_service(cls):

        api_key: str = os.getenv('API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube


class PlayList(MixinYouTube):

    def __init__(self, playlist_id):
        self.playlist_id = playlist_id
        playlist = self.get_service().playlists().list(id=self.playlist_id, part='snippet').execute()
        self.title = playlist['items'][0]['snippet']['title']
        self.url = f"https://www.youtube.com/playlist?list={self.playlist_id}"

    @property
    def total_duration(self):
        playlist_videos = self.get_service().playlistItems().list(playlistId=self.playlist_id, part='contentDetails', maxResults=50).execute()
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
        video_response = self.get_service().videos().list(part='contentDetails,statistics', id=','.join(video_ids)).execute()
        duration = timedelta()
        for video in video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration += isodate.parse_duration(iso_8601_duration)
        return duration

    def show_best_video(self):
        playlist_videos = self.get_service().playlistItems().list(playlistId=self.playlist_id, part='contentDetails', maxResults=50).execute()
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
        video_response = self.get_service().videos().list(part='contentDetails,statistics',id=','.join(video_ids)).execute()
        max_likes = 0
        video_id = ''
        for video in video_response['items']:
            like_count: int = int(video['statistics']['likeCount'])
            if like_count > max_likes:
                max_likes = like_count
                video_id = video['id']
        return f"https://youtu.be/{video_id}"




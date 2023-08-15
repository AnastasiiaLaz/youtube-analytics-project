import json
import os
from googleapiclient.discovery import build

import isodate

YT_API_KEY = 'AIzaSyB9owKVw7SBV925QMSK_qUQhArDFejcnec'


def printj(dict_to_print: dict) -> None:
    """Выводит словарь в json-подобном удобном формате с отступами"""
    print(json.dumps(dict_to_print, indent=2, ensure_ascii=False))


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.channel_id = channel_id
        self.api_key: str = os.getenv(YT_API_KEY)

    def get_channel_info(self):
        """
        Получает инфу о канале из YouTube API
        """
        youtube = build('youtube', 'v3', developerKey=self.api_key)
        channel = youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        if 'items' in channel:
            return channel['items'][0]
        return None

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        channel_info = self.get_channel_info()
        if channel_info:
            snippet = channel_info['snippet']
            statistics = channel_info['statisctics']
            channel_data = {"Название канала": snippet['title'],
                            "Описание": snippet['description'],
                            "Число подписчиков": statistics['subscriberCount'],
                            "Число просмотров": statistics['viewCount'],
                            "Ссылка на канал": f"https://www.youtube.com/channel/{self.channel_id}"}
            printj(channel_data)
        else:
            printj({"error": "Канал не найден или произошла ошибка при получении данных."})

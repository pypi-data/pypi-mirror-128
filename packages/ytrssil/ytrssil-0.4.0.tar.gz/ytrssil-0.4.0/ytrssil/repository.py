import os
from datetime import datetime
from sqlite3 import connect
from types import TracebackType
from typing import Any, Optional, Type

from inject import autoparams

from ytrssil.config import Configuration
from ytrssil.constants import config_dir
from ytrssil.datatypes import Channel, Video
from ytrssil.exceptions import ChannelNotFound
from ytrssil.protocols import ChannelRepository


class SqliteChannelRepository:
    def __init__(self) -> None:
        os.makedirs(config_dir, exist_ok=True)
        self.file_path: str = os.path.join(config_dir, 'channels.db')
        self.setup_database()

    def setup_database(self) -> None:
        connection = connect(self.file_path)
        cursor = connection.cursor()
        cursor.execute('PRAGMA foreign_keys = ON')
        cursor.execute(
            'CREATE TABLE IF NOT EXISTS channels ('
            'channel_id VARCHAR PRIMARY KEY, name VARCHAR)'
        )
        cursor.execute(
            'CREATE TABLE IF NOT EXISTS videos ('
            'video_id VARCHAR PRIMARY KEY, name VARCHAR, url VARCHAR UNIQUE, '
            'timestamp VARCHAR, watch_timestamp VARCHAR, channel_id VARCHAR, '
            'FOREIGN KEY(channel_id) REFERENCES channels(channel_id))'
        )
        connection.commit()
        connection.close()

    def __enter__(self) -> ChannelRepository:
        self.connection = connect(self.file_path)
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        self.connection.close()

    def channel_to_params(self, channel: Channel) -> dict[str, str]:
        return {
            'channel_id': channel.channel_id,
            'name': channel.name,
        }

    def channel_data_to_channel(
        self,
        channel_data: tuple[str, str, str],
    ) -> Channel:
        channel = Channel(
            channel_id=channel_data[0],
            name=channel_data[1],
        )
        for video in self.get_videos_for_channel(channel):
            if video.watch_timestamp is not None:
                channel.watched_videos[video.video_id] = video
            else:
                channel.new_videos[video.video_id] = video

        return channel

    def video_to_params(self, video: Video) -> dict[str, Any]:
        watch_timestamp: Optional[str]
        if video.watch_timestamp is not None:
            watch_timestamp = video.watch_timestamp.isoformat()
        else:
            watch_timestamp = video.watch_timestamp

        return {
            'video_id': video.video_id,
            'name': video.name,
            'url': video.url,
            'timestamp': video.timestamp.isoformat(),
            'watch_timestamp': watch_timestamp,
            'channel_id': video.channel_id,
        }

    def video_data_to_video(
        self,
        video_data: tuple[str, str, str, str, str],
        channel_id: str,
        channel_name: str,
    ) -> Video:
        watch_timestamp: Optional[datetime]
        if video_data[4] is not None:
            watch_timestamp = datetime.fromisoformat(video_data[4])
        else:
            watch_timestamp = video_data[4]

        return Video(
            video_id=video_data[0],
            name=video_data[1],
            url=video_data[2],
            timestamp=datetime.fromisoformat(video_data[3]),
            watch_timestamp=watch_timestamp,
            channel_id=channel_id,
            channel_name=channel_name,
        )

    def get_channel(self, channel_id: str) -> Channel:
        cursor = self.connection.cursor()
        cursor.execute(
            'SELECT * FROM channels WHERE channel_id=:channel_id',
            {'channel_id': channel_id},
        )
        try:
            return self.channel_data_to_channel(next(cursor))
        except StopIteration:
            raise ChannelNotFound

    def get_all_channels(self) -> list[Channel]:
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM channels')

        return [
            self.channel_data_to_channel(channel_data)
            for channel_data in cursor
        ]

    def get_videos_for_channel(
        self,
        channel: Channel,
    ) -> list[Video]:
        cursor = self.connection.cursor()
        cursor.execute(
            'SELECT video_id, name, url, timestamp, watch_timestamp '
            'FROM videos WHERE channel_id=:channel_id',
            {'channel_id': channel.channel_id},
        )

        return [
            self.video_data_to_video(
                video_data=video_data,
                channel_id=channel.channel_id,
                channel_name=channel.name,
            )
            for video_data in cursor
        ]

    def get_watched_videos(self) -> dict[str, Video]:
        cursor = self.connection.cursor()
        cursor.execute(
            'SELECT video_id, videos.name, url, timestamp, '
            'watch_timestamp, channels.channel_id, channels.name FROM videos '
            'LEFT JOIN channels ON channels.channel_id=videos.channel_id '
            'WHERE watch_timestamp IS NOT NULL ORDER BY timestamp'
        )

        return {
            video_data[0]: self.video_data_to_video(
                video_data=video_data,
                channel_id=video_data[5],
                channel_name=video_data[6],
            )
            for video_data in cursor
        }

    def get_new_videos(self) -> dict[str, Video]:
        cursor = self.connection.cursor()
        cursor.execute(
            'SELECT video_id, videos.name, url, timestamp, '
            'watch_timestamp, channels.channel_id, channels.name FROM videos '
            'LEFT JOIN channels ON channels.channel_id=videos.channel_id '
            'WHERE watch_timestamp IS NULL ORDER BY timestamp'
        )

        return {
            video_data[0]: self.video_data_to_video(
                video_data=video_data,
                channel_id=video_data[5],
                channel_name=video_data[6],
            )
            for video_data in cursor
        }

    def create_channel(self, channel: Channel) -> None:
        cursor = self.connection.cursor()
        cursor.execute(
            'INSERT INTO channels VALUES (:channel_id, :name)',
            self.channel_to_params(channel),
        )
        self.connection.commit()

    def update_channel(self, channel: Channel) -> None:
        cursor = self.connection.cursor()
        cursor.execute(
            'UPDATE channels SET channel_id = :channel_id, name = :name, '
            'WHERE channel_id=:channel_id',
            self.channel_to_params(channel),
        )
        self.connection.commit()

    def add_new_video(self, channel: Channel, video: Video) -> None:
        cursor = self.connection.cursor()
        cursor.execute(
            'INSERT INTO videos VALUES (:video_id, :name, '
            ':url, :timestamp, :watch_timestamp, :channel_id)',
            self.video_to_params(video),
        )
        self.connection.commit()

    def update_video(self, video: Video, watch_timestamp: datetime) -> None:
        cursor = self.connection.cursor()
        cursor.execute(
            'UPDATE videos SET watch_timestamp = :watch_timestamp '
            'WHERE video_id=:video_id',
            {
                'watch_timestamp': watch_timestamp.isoformat(),
                'video_id': video.video_id,
            },
        )
        self.connection.commit()


@autoparams()
def create_channel_repository(config: Configuration) -> ChannelRepository:
    repo_type = config.channel_repository_type
    if repo_type == 'sqlite':
        return SqliteChannelRepository()
    else:
        raise Exception(f'Unknown channel repository type: "{repo_type}"')

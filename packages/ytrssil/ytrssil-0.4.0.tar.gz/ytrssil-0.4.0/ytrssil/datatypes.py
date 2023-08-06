from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional, TypedDict


class VideoData(TypedDict):
    video_id: str
    name: str
    url: str
    channel_id: str
    channel_name: str
    timestamp: datetime
    watch_timestamp: Optional[datetime]


class ChannelData(TypedDict):
    channel_id: str
    name: str
    new_videos: dict[str, Any]
    watched_videos: dict[str, Any]


@dataclass
class Video:
    video_id: str
    name: str
    url: str
    channel_id: str
    channel_name: str
    timestamp: datetime
    watch_timestamp: Optional[datetime] = None

    def __str__(self) -> str:
        return f'{self.channel_name} - {self.name} - {self.video_id}'

    @classmethod
    def from_dict(cls, data: VideoData) -> Video:
        return cls(**data)


@dataclass
class Channel:
    channel_id: str
    name: str
    new_videos: dict[str, Video] = field(default_factory=lambda: dict())
    watched_videos: dict[str, Video] = field(default_factory=lambda: dict())

    def add_video(self, video: Video) -> bool:
        if (
            video.video_id in self.watched_videos
            or video.video_id in self.new_videos
        ):
            return False

        self.new_videos[video.video_id] = video
        return True

    def mark_video_as_watched(self, video: Video) -> None:
        self.new_videos.pop(video.video_id)
        self.watched_videos[video.video_id] = video

    def __str__(self) -> str:
        return f'{self.name} - {len(self.new_videos)}'

    @classmethod
    def from_dict(cls, data: ChannelData) -> Channel:
        return cls(
            channel_id=data['channel_id'],
            name=data['name'],
            new_videos=data.get('new_videos', {}).copy(),
            watched_videos=data.get('watched_videos', {}).copy(),
        )

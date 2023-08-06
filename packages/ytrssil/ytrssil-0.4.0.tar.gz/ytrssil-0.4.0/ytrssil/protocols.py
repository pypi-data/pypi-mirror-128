from __future__ import annotations

from datetime import datetime
from types import TracebackType
from typing import Iterable, Optional, Protocol, Type

from ytrssil.config import Configuration
from ytrssil.datatypes import Channel, Video


class ChannelRepository(Protocol):
    def __enter__(self) -> ChannelRepository:  # pragma: no cover
        ...

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:  # pragma: no cover
        ...

    def get_channel(self, channel_id: str) -> Channel:  # pragma: no cover
        ...

    def get_all_channels(self) -> list[Channel]:  # pragma: no cover
        ...

    def get_watched_videos(self) -> dict[str, Video]:  # pragma: no cover
        ...

    def get_new_videos(self) -> dict[str, Video]:  # pragma: no cover
        ...

    def create_channel(self, channel: Channel) -> None:  # pragma: no cover
        ...

    def add_new_video(
        self,
        channel: Channel,
        video: Video,
    ) -> None:  # pragma: no cover
        ...

    def update_video(
        self,
        video: Video,
        watch_timestamp: datetime,
    ) -> None:  # pragma: no cover
        ...


class Fetcher(Protocol):
    def fetch_feeds(
        self,
        urls: Iterable[str],
    ) -> Iterable[str]:  # pragma: no cover
        ...

    def fetch_new_videos(
        self,
        config: Optional[Configuration] = None,
        parser: Optional[Parser] = None,
    ) -> tuple[dict[str, Channel], dict[str, Video]]:  # pragma: no cover
        ...


class Parser(Protocol):
    def __call__(self, feed_content: str) -> Channel:  # pragma: no cover
        ...

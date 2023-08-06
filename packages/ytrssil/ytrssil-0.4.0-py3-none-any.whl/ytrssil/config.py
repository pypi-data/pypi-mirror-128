from __future__ import annotations

import os
from collections.abc import Iterator
from dataclasses import dataclass, field
from typing import Any

from ytrssil.constants import config_dir


@dataclass
class Configuration:
    feed_url_getter_type: str = 'file'
    feed_urls: list[str] = field(default_factory=lambda: list())
    channel_repository_type: str = 'sqlite'
    fetcher_type: str = 'aiohttp'
    parser_type: str = 'feedparser'

    @classmethod
    def from_dict(cls, config_dict: dict[str, Any]) -> Configuration:
        return cls(**config_dict)

    def get_feed_urls(self) -> Iterator[str]:
        if self.feed_url_getter_type == 'file':
            file_path = os.path.join(config_dir, 'feeds')
            with open(file_path, 'r') as f:
                for line in f:
                    yield line.strip()
        elif self.feed_url_getter_type == 'static':
            yield from self.feed_urls

from datetime import datetime

import feedparser
from inject import autoparams

from ytrssil.config import Configuration
from ytrssil.datatypes import Channel, Video
from ytrssil.exceptions import ChannelNotFound
from ytrssil.protocols import ChannelRepository, Parser


class ParserBase:
    @autoparams('channel_repository')
    def __init__(self, channel_repository: ChannelRepository) -> None:
        self.repository = channel_repository


class FeedparserParser(ParserBase):
    def __call__(self, feed_content: str) -> Channel:
        d = feedparser.parse(feed_content)
        channel_id: str = d['feed']['yt_channelid']
        try:
            channel = self.repository.get_channel(channel_id)
        except ChannelNotFound:
            channel = Channel(
                channel_id=channel_id,
                name=d['feed']['title'],
            )
            self.repository.create_channel(channel)

        for entry in d['entries']:
            video = Video(
                video_id=entry['yt_videoid'],
                name=entry['title'],
                url=entry['link'],
                timestamp=datetime.fromisoformat(entry['published']),
                channel_id=channel.channel_id,
                channel_name=channel.name,
            )
            if channel.add_video(video):
                self.repository.add_new_video(channel, video)

        return channel


@autoparams()
def create_feed_parser(config: Configuration) -> Parser:
    parser_type = config.parser_type
    if parser_type == 'feedparser':
        return FeedparserParser()
    else:
        raise Exception(f'Unknown feed parser type: "{parser_type}"')

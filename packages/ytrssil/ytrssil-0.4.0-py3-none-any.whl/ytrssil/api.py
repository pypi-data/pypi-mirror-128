from inject import autoparams

from ytrssil.bindings import setup_dependencies
from ytrssil.datatypes import Video
from ytrssil.protocols import ChannelRepository, Fetcher


def get_new_videos() -> list[Video]:
    setup_dependencies()

    @autoparams()
    def _get_new_videos(
        repository_manager: ChannelRepository,
        fetcher: Fetcher,
    ) -> dict[str, Video]:
        with repository_manager as _:
            _, new_videos = fetcher.fetch_new_videos()
            return new_videos

    return list(_get_new_videos().values())


def get_new_video_count() -> int:
    return len(get_new_videos())

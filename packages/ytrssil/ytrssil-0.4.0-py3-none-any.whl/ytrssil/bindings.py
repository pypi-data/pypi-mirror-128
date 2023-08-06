from inject import Binder, Injector, clear_and_configure, get_injector_or_die

from ytrssil.config import Configuration
from ytrssil.fetch import create_fetcher
from ytrssil.parse import create_feed_parser
from ytrssil.protocols import ChannelRepository, Fetcher, Parser
from ytrssil.repository import create_channel_repository


def dependency_configuration(binder: Binder) -> None:
    config = Configuration()
    binder.bind(Configuration, config)
    binder.bind_to_constructor(ChannelRepository, create_channel_repository)
    binder.bind_to_constructor(Fetcher, create_fetcher)
    binder.bind_to_constructor(Parser, create_feed_parser)


def setup_dependencies() -> Injector:
    clear_and_configure(dependency_configuration)

    return get_injector_or_die()

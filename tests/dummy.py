from playwright.async_api import Browser as AsyncBrowser
from playwright.sync_api import Browser as SyncBrowser


class DummySyncBrowser(SyncBrowser):
    """A dummy Browser for testing."""

    def __init__(self) -> None:
        pass


class DummyAsyncBrowser(AsyncBrowser):
    """A dummy Browser for testing."""

    def __init__(self) -> None:
        pass

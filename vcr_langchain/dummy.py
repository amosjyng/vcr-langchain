import os

from langchain_community.tools.playwright.utils import (
    create_async_playwright_browser,
    create_sync_playwright_browser,
)
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


def get_sync_test_browser(cassette_path: str, headless: bool = False) -> SyncBrowser:
    if os.path.exists(cassette_path):
        return DummySyncBrowser()
    else:
        return create_sync_playwright_browser(headless=headless)


def get_async_test_browser(cassette_path: str, headless: bool = False) -> AsyncBrowser:
    if os.path.exists(cassette_path):
        return DummyAsyncBrowser()
    else:
        return create_async_playwright_browser(headless=headless)

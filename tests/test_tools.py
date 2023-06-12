import os

import nest_asyncio
from langchain.python import PythonREPL
from langchain.serpapi import SerpAPIWrapper
from langchain.tools.playwright.navigate import NavigateTool
from langchain.tools.playwright.utils import (
    create_async_playwright_browser,
    create_sync_playwright_browser,
)
from langchain.utilities.bash import BashProcess
from playwright.async_api import Browser as AsyncBrowser
from playwright.sync_api import Browser as SyncBrowser

import vcr_langchain as vcr
from tests import TemporaryCassettePath
from tests.dummy import DummyAsyncBrowser, DummySyncBrowser


@vcr.use_cassette()
def test_use_serp_api() -> None:
    answer = SerpAPIWrapper().run(query="how far is the moon receding every year")
    assert answer == "about 3.78 cm per year"


@vcr.use_cassette()
def test_use_serp_api_without_keyword() -> None:
    answer = SerpAPIWrapper().run("how big is the sun")
    assert answer == "432,690 mi"


def test_use_python_repl() -> None:
    cassette_path = "python-with-keyword.yaml"
    with TemporaryCassettePath(cassette_path):
        with vcr.use_cassette(cassette_path):
            answer = PythonREPL().run(command="print(5 * 4)")
            assert answer.strip() == "20"


def test_use_python_repl_without_keyword() -> None:
    cassette_path = "python-no-keyword.yaml"
    with TemporaryCassettePath(cassette_path):
        with vcr.use_cassette(cassette_path):
            answer = PythonREPL().run("print(5 - 4)")
            assert answer.strip() == "1"


def test_use_python_repl_regularly() -> None:
    answer = PythonREPL().run("print(5 + 4)")
    assert answer.strip() == "9"


@vcr.use_cassette()
def test_use_bash() -> None:
    time = BashProcess().run("date")
    assert time == "Fri Feb  3 13:05:45 +07 2023\n"


@vcr.use_cassette()
def test_use_bash_multiple_commands() -> None:
    test_filename = "tests/asdf"
    results = BashProcess().run(
        [
            f"touch {test_filename}",
            f"ls {test_filename}",
            f"rm {test_filename}",
        ]
    )
    assert results == "tests/asdf\n"


@vcr.use_cassette()
def test_use_bash_same_commands() -> None:
    test_filename = "tests/bsdf"
    bash = BashProcess()
    old_results = bash.run(f"ls {test_filename}")
    assert "returned non-zero exit status 2" in old_results
    bash.run(f"touch {test_filename}")
    new_results = bash.run(f"ls {test_filename}")
    assert new_results == "tests/bsdf\n"
    bash.run(f"rm {test_filename}")


@vcr.use_cassette(path="tests/playwright-sync.yaml")
def test_use_playwright_sync_tools() -> None:
    if os.path.exists("tests/playwright-sync.yaml"):
        # skip browser initialization and check that test still works
        browser: SyncBrowser = DummySyncBrowser()
    else:
        browser = create_sync_playwright_browser(headless=False)
    navigate = NavigateTool.from_browser(sync_browser=browser)
    result = navigate.run("https://www.google.com/")
    assert result == "Navigating to https://www.google.com/ returned status code 200"


@vcr.use_cassette(path="tests/playwright-async.yaml")
async def test_use_playwright_async_tools() -> None:
    nest_asyncio.apply()

    if os.path.exists("tests/playwright-async.yaml"):
        # skip browser initialization and check that test still works
        browser: AsyncBrowser = DummyAsyncBrowser()
    else:
        browser = create_async_playwright_browser(headless=False)
    navigate = NavigateTool.from_browser(async_browser=browser)
    result = await navigate.arun("https://www.google.com/")
    assert result == "Navigating to https://www.google.com/ returned status code 200"

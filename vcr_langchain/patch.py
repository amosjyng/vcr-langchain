import itertools
import logging
from typing import Any, Callable, Iterable, List, Optional, Sequence

from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain.python import PythonREPL
from langchain.tools.playwright.click import ClickTool
from langchain.tools.playwright.current_page import CurrentWebPageTool
from langchain.tools.playwright.extract_hyperlinks import ExtractHyperlinksTool
from langchain.tools.playwright.extract_text import ExtractTextTool
from langchain.tools.playwright.get_elements import GetElementsTool
from langchain.tools.playwright.navigate import NavigateTool
from langchain.tools.playwright.navigate_back import NavigateBackTool
from vcr.cassette import Cassette
from vcr.patch import CassettePatcherBuilder

from .generic import GenericPatch

log = logging.getLogger(__name__)


CUSTOM_PATCHERS: List[Any] = []


def add_patchers(*patchers: Any) -> None:
    CUSTOM_PATCHERS.extend(patchers)


class PythonREPLPatch(GenericPatch):
    def __init__(self, cassette: Cassette):
        super().__init__(cassette, PythonREPL, "run")

    def get_same_signature_override(self) -> Callable:
        def run(og_self: PythonREPL, command: str) -> str:
            """Same signature override patched into PythonREPL"""
            return self.generic_override(og_self, command=command)

        return run


class NavigateToolPatch(GenericPatch):
    def __init__(self, cassette: Cassette):
        super().__init__(cassette, NavigateTool, "_run")

    def get_same_signature_override(self) -> Callable:
        def run(
            og_self: NavigateTool,
            url: str,
            run_manager: Optional[CallbackManagerForToolRun] = None,
        ) -> str:
            return self.generic_override(og_self, url=url, run_manager=run_manager)

        return run


class NavigateToolAsyncPatch(GenericPatch):
    def __init__(self, cassette: Cassette):
        super().__init__(cassette, NavigateTool, "_arun")

    def get_same_signature_override(self) -> Callable:
        async def arun(
            og_self: NavigateTool,
            url: str,
            run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
        ) -> str:
            return await self.generic_override(
                og_self, url=url, run_manager=run_manager
            )

        return arun


class ClickToolPatch(GenericPatch):
    def __init__(self, cassette: Cassette):
        super().__init__(cassette, ClickTool, "_run")

    def get_same_signature_override(self) -> Callable:
        def run(
            og_self: ClickTool,
            selector: str,
            run_manager: Optional[CallbackManagerForToolRun] = None,
        ) -> str:
            return self.generic_override(
                og_self, selector=selector, run_manager=run_manager
            )

        return run


class ClickToolAsyncPatch(GenericPatch):
    def __init__(self, cassette: Cassette):
        super().__init__(cassette, ClickTool, "_arun")

    def get_same_signature_override(self) -> Callable:
        async def arun(
            og_self: ClickTool,
            selector: str,
            run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
        ) -> str:
            return await self.generic_override(
                og_self, selector=selector, run_manager=run_manager
            )

        return arun


class CurrentWebPageToolPatch(GenericPatch):
    def __init__(self, cassette: Cassette):
        super().__init__(cassette, CurrentWebPageTool, "_run")

    def get_same_signature_override(self) -> Callable:
        def run(
            og_self: CurrentWebPageTool,
            run_manager: Optional[CallbackManagerForToolRun] = None,
        ) -> str:
            return self.generic_override(og_self, run_manager=run_manager)

        return run


class CurrentWebPageToolAsyncPatch(GenericPatch):
    def __init__(self, cassette: Cassette):
        super().__init__(cassette, CurrentWebPageTool, "_arun")

    def get_same_signature_override(self) -> Callable:
        async def arun(
            og_self: CurrentWebPageTool,
            run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
        ) -> str:
            return await self.generic_override(og_self, run_manager=run_manager)

        return arun


class ExtractHyperlinksToolPatch(GenericPatch):
    def __init__(self, cassette: Cassette):
        super().__init__(cassette, ExtractHyperlinksTool, "_run")

    def get_same_signature_override(self) -> Callable:
        def run(
            og_self: ExtractHyperlinksTool,
            absolute_urls: bool = False,
            run_manager: Optional[CallbackManagerForToolRun] = None,
        ) -> str:
            return self.generic_override(
                og_self, absolute_urls=absolute_urls, run_manager=run_manager
            )

        return run


class ExtractHyperlinksToolAsyncPatch(GenericPatch):
    def __init__(self, cassette: Cassette):
        super().__init__(cassette, ExtractHyperlinksTool, "_arun")

    def get_same_signature_override(self) -> Callable:
        async def arun(
            og_self: ExtractHyperlinksTool,
            absolute_urls: bool = False,
            run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
        ) -> str:
            return await self.generic_override(
                og_self,
                absolute_urls=absolute_urls,
                run_manager=run_manager,
            )

        return arun


class ExtractTextToolPatch(GenericPatch):
    def __init__(self, cassette: Cassette):
        super().__init__(cassette, ExtractTextTool, "_run")

    def get_same_signature_override(self) -> Callable:
        def run(
            og_self: ExtractTextTool,
            run_manager: Optional[CallbackManagerForToolRun] = None,
        ) -> str:
            return self.generic_override(og_self, run_manager=run_manager)

        return run


class ExtractTextToolAsyncPatch(GenericPatch):
    def __init__(self, cassette: Cassette):
        super().__init__(cassette, ExtractTextTool, "_arun")

    def get_same_signature_override(self) -> Callable:
        async def arun(
            og_self: ExtractTextTool,
            run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
        ) -> str:
            return await self.generic_override(og_self, run_manager=run_manager)

        return arun


class GetElementsToolPatch(GenericPatch):
    def __init__(self, cassette: Cassette):
        super().__init__(cassette, GetElementsTool, "_run")

    def get_same_signature_override(self) -> Callable:
        def run(
            og_self: GetElementsTool,
            selector: str,
            attributes: Sequence[str] = ["innerText"],
            run_manager: Optional[CallbackManagerForToolRun] = None,
        ) -> str:
            return self.generic_override(
                og_self,
                selector=selector,
                attributes=attributes,
                run_manager=run_manager,
            )

        return run


class GetElementsToolAsyncPatch(GenericPatch):
    def __init__(self, cassette: Cassette):
        super().__init__(cassette, GetElementsTool, "_arun")

    def get_same_signature_override(self) -> Callable:
        async def arun(
            og_self: GetElementsTool,
            selector: str,
            attributes: Sequence[str] = ["innerText"],
            run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
        ) -> str:
            return await self.generic_override(
                og_self,
                selector=selector,
                attributes=attributes,
                run_manager=run_manager,
            )

        return arun


class NavigateBackToolPatch(GenericPatch):
    def __init__(self, cassette: Cassette):
        super().__init__(cassette, NavigateBackTool, "_run")

    def get_same_signature_override(self) -> Callable:
        def run(
            og_self: NavigateBackTool,
            run_manager: Optional[CallbackManagerForToolRun] = None,
        ) -> str:
            return self.generic_override(og_self, run_manager=run_manager)

        return run


class NavigateBackToolAsyncPatch(GenericPatch):
    def __init__(self, cassette: Cassette):
        super().__init__(cassette, NavigateBackTool, "_arun")

    def get_same_signature_override(self) -> Callable:
        async def arun(
            og_self: NavigateBackTool,
            run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
        ) -> str:
            return await self.generic_override(og_self, run_manager=run_manager)

        return arun


def get_overridden_build(og_build: Callable) -> Callable:
    def build(og_self: CassettePatcherBuilder) -> Iterable[Any]:
        patches = [patcher(og_self._cassette) for patcher in CUSTOM_PATCHERS]
        return itertools.chain(og_build(og_self), patches)

    return build


CassettePatcherBuilder.build = get_overridden_build(CassettePatcherBuilder.build)
# add this after overriding the above build function, to make sure that users of this
# library can also add their own custom patchers in
add_patchers(
    PythonREPLPatch,
    NavigateToolPatch,
    NavigateToolAsyncPatch,
    ClickToolPatch,
    ClickToolAsyncPatch,
    CurrentWebPageToolPatch,
    CurrentWebPageToolAsyncPatch,
    ExtractHyperlinksToolPatch,
    ExtractHyperlinksToolAsyncPatch,
    ExtractTextToolPatch,
    ExtractTextToolAsyncPatch,
    GetElementsToolPatch,
    GetElementsToolAsyncPatch,
    NavigateBackToolPatch,
    NavigateBackToolAsyncPatch,
)

try:
    from .bash_patch import BashProcessPatch

    add_patchers(BashProcessPatch)
except ImportError:
    pass

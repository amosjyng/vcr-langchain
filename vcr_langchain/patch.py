import logging

import langchain
from langchain.python import PythonREPL
from langchain.serpapi import SerpAPIWrapper
from vcr.patch import CassettePatcherBuilder as OgCassettePatcherBuilder

from .cache import VcrCache
from .request import Request

log = logging.getLogger(__name__)


class CachePatch:
    def __init__(self, cassette):
        self.cassette = cassette

    def __enter__(self):
        langchain.llm_cache = VcrCache(self.cassette)

    def __exit__(self, *args):
        langchain.llm_cache = None


class GenericPatch:
    """
    Generic class for patching into tool overrides

    Inherit from this, and ideally create a copy of the function you're patching in
    order to ensure that everything always gets converted into kwargs for
    serialization. See SerpPatch as an example of what to do.
    """

    def __init__(self, cassette, cls, fn_name):
        self.cassette = cassette
        self.cls = cls
        self.fn_name = fn_name
        self.og_fn = getattr(cls, fn_name)
        self.generic_override = self.get_generic_override_fn()
        self.same_signature_override = self.get_same_signature_override()

    def get_generic_override_fn(self):
        def fn_override(og_self, **kwargs):
            request = Request(tool=self.cls.__name__, **kwargs)
            cached_response = self.cassette.lookup(request)
            if cached_response:
                return cached_response

            new_response = self.og_fn(og_self, **kwargs)
            self.cassette.append(request, new_response)
            return new_response

        return fn_override

    def get_same_signature_override(self):
        """Override this function in the inherited class to convert args to kwargs"""
        return self.get_generic_override_fn()

    def __enter__(self):
        setattr(self.cls, self.fn_name, self.same_signature_override)

    def __exit__(self, *args):
        setattr(self.cls, self.fn_name, self.og_fn)


class SerpPatch(GenericPatch):
    def __init__(self, cassette):
        super().__init__(cassette, SerpAPIWrapper, "run")

    def get_same_signature_override(self):
        def run(og_self, query: str) -> str:
            return self.generic_override(og_self, query=query)

        return run


class PythonREPLPatch(GenericPatch):
    def __init__(self, cassette):
        super().__init__(cassette, PythonREPL, "run")

    def get_same_signature_override(self):
        def run(og_self, command: str) -> str:
            return self.generic_override(og_self, command=command)

        return run


class CassettePatcherBuilder(OgCassettePatcherBuilder):
    def build(self):
        return (
            CachePatch(self._cassette),
            SerpPatch(self._cassette),
            PythonREPLPatch(self._cassette),
        )

import logging

import gorilla
import langchain
from langchain.python import PythonREPL
from langchain.serpapi import SerpAPIWrapper
from vcr.patch import CassettePatcherBuilder as OgCassettePatcherBuilder

from .cache import VcrCache
from .request import Request

log = logging.getLogger(__name__)


LANGCHAIN_VISUALIZER_PATCH_ID = "lc-viz"
VCR_LANGCHAIN_PATCH_ID = "lc-vcr"
# override prefix to use if langchain-visualizer is there as well
VCR_VIZ_INTEROP_PREFIX = "_vcr_"


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

        # if the backup for the OG function has already been set, then that most likely
        # means langchain visualizer got to it first. we'll let the visualizer call out
        # to us because we always want to visualize a call even if it's cached -- we
        # don't want to hide cached calls in the visualization graph
        viz_was_here = False
        try:
            self.og_fn = gorilla.get_original_attribute(
                self.cls, self.fn_name, LANGCHAIN_VISUALIZER_PATCH_ID
            )
            viz_was_here = True
        except AttributeError:
            self.og_fn = getattr(self.cls, self.fn_name)

        self.generic_override = self.get_generic_override_fn()
        self.same_signature_override = self.get_same_signature_override()
        override_name = (
            VCR_VIZ_INTEROP_PREFIX + self.fn_name if viz_was_here else self.fn_name
        )
        self.patch = gorilla.Patch(
            destination=self.cls,
            name=override_name,
            obj=self.same_signature_override,
            settings=gorilla.Settings(store_hit=True, allow_hit=not viz_was_here),
        )

    def get_generic_override_fn(self):
        def fn_override(og_self, **kwargs):
            """Actual override functionality"""
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
        gorilla.apply(self.patch, id=VCR_LANGCHAIN_PATCH_ID)

    def __exit__(self, *args):
        gorilla.revert(self.patch)


class SerpPatch(GenericPatch):
    def __init__(self, cassette):
        super().__init__(cassette, SerpAPIWrapper, "run")

    def get_same_signature_override(self):
        def run(og_self, query: str) -> str:
            """Same signature override patched into SerpAPIWrapper"""
            return self.generic_override(og_self, query=query)

        return run


class PythonREPLPatch(GenericPatch):
    def __init__(self, cassette):
        super().__init__(cassette, PythonREPL, "run")

    def get_same_signature_override(self):
        def run(og_self, command: str) -> str:
            """Same signature override patched into PythonREPL"""
            return self.generic_override(og_self, command=command)

        return run


class CassettePatcherBuilder(OgCassettePatcherBuilder):
    def build(self):
        return (
            CachePatch(self._cassette),
            SerpPatch(self._cassette),
            PythonREPLPatch(self._cassette),
        )

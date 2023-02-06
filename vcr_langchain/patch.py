import itertools
import json
import logging
from typing import Any, Callable, Iterable, List, Optional, Type, Union

import gorilla
from langchain.python import PythonREPL
from langchain.utilities.bash import BashProcess
from vcr.cassette import Cassette
from vcr.errors import CannotOverwriteExistingCassetteException
from vcr.patch import CassettePatcherBuilder
from vcr.request import Request

log = logging.getLogger(__name__)


LANGCHAIN_VISUALIZER_PATCH_ID = "lc-viz"
VCR_LANGCHAIN_PATCH_ID = "lc-vcr"
# override prefix to use if langchain-visualizer is there as well
VCR_VIZ_INTEROP_PREFIX = "_vcr_"


CUSTOM_PATCHERS: List[Any] = []


def add_patchers(*patchers: Any) -> None:
    CUSTOM_PATCHERS.extend(patchers)


log = logging.getLogger(__name__)


def lookup(cassette: Cassette, request: Request) -> Optional[Any]:
    """
    Code modified from OG vcrpy:
    https://github.com/kevin1024/vcrpy/blob/v4.2.1/vcr/stubs/__init__.py#L225
    """
    if cassette.can_play_response_for(request):
        log.info("Playing response for {} from cassette".format(request))
        return cassette.play_response(request)
    else:
        if cassette.write_protected and cassette.filter_request(request):
            raise CannotOverwriteExistingCassetteException(
                cassette=cassette, failed_request=request
            )
        return None


class GenericPatch:
    """
    Generic class for patching into tool overrides

    Inherit from this, and ideally create a copy of the function you're patching in
    order to ensure that everything always gets converted into kwargs for
    serialization. See PythonREPLPatch as an example of what to do.
    """

    def __init__(self, cassette: Cassette, cls: Type, fn_name: str):
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

    def get_generic_override_fn(self) -> Callable:
        def fn_override(og_self: Any, **kwargs: str) -> Any:
            """Actual override functionality"""
            tool_name = self.cls.__name__
            fake_uri = f"tool://{tool_name}"
            request = Request(
                method="POST",
                uri=fake_uri,
                body=json.dumps(kwargs, sort_keys=True),
                headers={},
            )
            cached_response = lookup(self.cassette, request)
            if cached_response is not None:
                return cached_response

            new_response = self.og_fn(og_self, **kwargs)
            self.cassette.append(request, new_response)
            return new_response

        return fn_override

    def get_same_signature_override(self) -> Callable:
        """Override this function in the inherited class to convert args to kwargs"""
        return self.get_generic_override_fn()

    def __enter__(self) -> None:
        gorilla.apply(self.patch, id=VCR_LANGCHAIN_PATCH_ID)

    def __exit__(self, *_: List[Any]) -> None:
        gorilla.revert(self.patch)


class PythonREPLPatch(GenericPatch):
    def __init__(self, cassette: Cassette):
        super().__init__(cassette, PythonREPL, "run")

    def get_same_signature_override(self) -> Callable:
        def run(og_self: PythonREPL, command: str) -> str:
            """Same signature override patched into PythonREPL"""
            return self.generic_override(og_self, command=command)

        return run


class BashProcessPatch(GenericPatch):
    def __init__(self, cassette: Cassette):
        super().__init__(cassette, BashProcess, "run")

    def get_same_signature_override(self) -> Callable:
        def run(og_self: BashProcess, commands: Union[str, List[str]]) -> str:
            """Same signature override patched into BashProcess"""
            return self.generic_override(og_self, commands=commands)

        return run


def get_overridden_build(og_build: Callable) -> Callable:
    def build(og_self: CassettePatcherBuilder) -> Iterable[Any]:
        patches = [patcher(og_self._cassette) for patcher in CUSTOM_PATCHERS]
        return itertools.chain(og_build(og_self), patches)

    return build


CassettePatcherBuilder.build = get_overridden_build(CassettePatcherBuilder.build)
# add this after overriding the above build function, to make sure that users of this
# library can also add their own custom patchers in
add_patchers(PythonREPLPatch, BashProcessPatch)

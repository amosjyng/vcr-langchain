import functools
from typing import Any, Dict, Tuple

from vcr import VCR as OgVCR

from . import matchers
from .cassette import Cassette, CassetteContextDecorator


class VCR(OgVCR):
    """
    A VCR that records and replays LLM and tool interactions instead of HTTP requests
    """

    def __init__(self, match_on: Tuple[str, ...] = ("all",), **kwargs: Dict[str, Any]):
        super().__init__(match_on=match_on, **kwargs)
        self.matchers = {
            "all": matchers.match_all,
        }

    def _use_cassette(
        self, with_current_defaults: bool = False, **kwargs: Dict[str, Any]
    ) -> CassetteContextDecorator:
        """Copied from the OG VCR class, except that this uses our own Cassette class"""
        if with_current_defaults:
            config = self.get_merged_config(**kwargs)
            return Cassette.use(**config)
        # This is made a function that evaluates every time a cassette
        # is made so that changes that are made to this VCR instance
        # that occur AFTER the `use_cassette` decorator is applied
        # still affect subsequent calls to the decorated function.
        args_getter = functools.partial(self.get_merged_config, **kwargs)
        return Cassette.use_arg_getter(args_getter)

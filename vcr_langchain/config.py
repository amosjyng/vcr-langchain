import functools

from vcr import VCR as OgVCR

from . import matchers
from .cassette import Cassette


class VCR(OgVCR):
    """A VCR that records and replays LLM interactions instead of HTTP requests"""

    def __init__(self, match_on=("prompt", "llm_string"), **kwargs):
        super().__init__(match_on=match_on, **kwargs)
        self.matchers = {
            "prompt": matchers.prompt,
            "llm_string": matchers.llm_string,
        }

    def _use_cassette(self, with_current_defaults=False, **kwargs):
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

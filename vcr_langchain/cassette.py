import contextlib

from vcr.cassette import Cassette as OgCassette
from vcr.cassette import CassetteContextDecorator as OgCassetteContextDecorator

from .matchers import llm_string, prompt
from .patch import CassettePatcherBuilder


class CassetteContextDecorator(OgCassetteContextDecorator):
    def _patch_generator(self, cassette):
        """
        Modified from OG _patch_generator. We need this to override the usage of the OG
        CassettePatcherBuilder in the function, but the TODO is fixed in the vcrpy
        master branch, so this may well stop working in the next release of vcrpy
        """
        with contextlib.ExitStack() as exit_stack:
            for patcher in CassettePatcherBuilder(cassette).build():
                exit_stack.enter_context(patcher)
            yield cassette
            # TODO(@IvanMalison): Hmmm. it kind of feels like this should be
            # somewhere else.
            cassette._save()


class Cassette(OgCassette):
    def __init__(self, match_on=(prompt, llm_string), **kwargs):
        super().__init__(match_on=match_on, **kwargs)

    @classmethod
    def use_arg_getter(cls, arg_getter):
        return CassetteContextDecorator(cls, arg_getter)

    @classmethod
    def use(cls, **kwargs):
        return CassetteContextDecorator.from_args(cls, **kwargs)

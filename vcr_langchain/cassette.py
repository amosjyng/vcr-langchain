import contextlib
import logging

from vcr.cassette import Cassette as OgCassette
from vcr.cassette import CassetteContextDecorator as OgCassetteContextDecorator
from vcr.errors import CannotOverwriteExistingCassetteException

from .matchers import match_all
from .patch import CassettePatcherBuilder

log = logging.getLogger(__name__)


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
    def __init__(self, match_on=(match_all,), **kwargs):
        super().__init__(match_on=match_on, **kwargs)

    @classmethod
    def use_arg_getter(cls, arg_getter):
        return CassetteContextDecorator(cls, arg_getter)

    @classmethod
    def use(cls, **kwargs):
        return CassetteContextDecorator.from_args(cls, **kwargs)

    def lookup(self, request):
        """
        Code modified from OG vcrpy:
        https://github.com/kevin1024/vcrpy/blob/v4.2.1/vcr/stubs/__init__.py#L225
        """
        if self.can_play_response_for(request):
            log.info("Playing response for {} from cassette".format(request))
            return self.play_response(request)
        else:
            if self.write_protected and self.filter_request(request):
                raise CannotOverwriteExistingCassetteException(
                    cassette=self, failed_request=request
                )
            return None

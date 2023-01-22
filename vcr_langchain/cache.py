import logging
from typing import Optional

from langchain.cache import RETURN_VAL_TYPE, BaseCache
from vcr.cassette import Cassette
from vcr.errors import CannotOverwriteExistingCassetteException

from .request import Request

log = logging.getLogger(__name__)


class VcrCache(BaseCache):
    """Cache that hooks into VCR functionality"""

    def __init__(self, cassette: Cassette) -> None:
        """Initialize with possibly pre-existing cassette."""
        self.cassette = cassette

    def lookup(self, prompt: str, llm_string: str) -> Optional[RETURN_VAL_TYPE]:
        """Look up based on prompt and llm_string."""
        request = Request(prompt=prompt, llm_string=llm_string)
        if self.cassette.can_play_response_for(request):
            log.info("Playing response for {} from cassette".format(request))
            return self.cassette.play_response(request)
        else:
            if self.cassette.write_protected and self.cassette.filter_request(request):
                raise CannotOverwriteExistingCassetteException(
                    cassette=self.cassette, failed_request=request
                )
            return None

    def update(self, prompt: str, llm_string: str, return_val: RETURN_VAL_TYPE) -> None:
        """Update cache based on prompt and llm_string."""
        if self.cassette.write_protected:
            raise CannotOverwriteExistingCassetteException(
                cassette=self.cassette, failed_request=None
            )

        request = Request(prompt=prompt, llm_string=llm_string)
        self.cassette.append(request, return_val)

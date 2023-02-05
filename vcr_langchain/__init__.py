from typing import Any, Callable, Dict, Union

from vcr import VCR, mode  # noqa

from .patch import get_overridden_build  # noqa


def scrub_header(header: str, replacement: str = "") -> Callable:
    def before_record_response(response: Union[Dict, Any]) -> Union[Dict, Any]:
        if isinstance(response, dict):
            if header in response["headers"]:
                response["headers"][header] = replacement
        return response

    return before_record_response


default_vcr = VCR(
    path_transformer=VCR.ensure_suffix(".yaml"),
    filter_headers=["authorization", "X-OpenAI-Client-User-Agent"],
    filter_query_parameters=["api_key"],
    before_record_response=scrub_header(
        "Openai-Organization", replacement="user-dummy"
    ),
    match_on=("method", "scheme", "host", "port", "path", "query", "body"),
)

use_cassette = default_vcr.use_cassette

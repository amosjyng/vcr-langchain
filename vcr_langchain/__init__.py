from typing import Any, Callable, Dict, Union

from vcr import VCR, mode

from .patch import get_overridden_build


def scrub_header(header: str, replacement: str = "") -> Callable:
    def before_record_response(response: Union[Dict, Any]) -> Union[Dict, Any]:
        if isinstance(response, dict):
            try:
                response_str = (
                    response.get("body", {}).get("string", b"").decode("utf-8")
                )
                if "Rate limit reached for" in response_str:
                    # don't record rate-limiting responses
                    return None
            except UnicodeDecodeError:
                pass  # ignore if we can't parse response

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
    record_mode=mode.ONCE,
)

use_cassette = default_vcr.use_cassette


__all__ = [
    "get_overridden_build",
]

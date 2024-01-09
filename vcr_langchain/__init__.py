from typing import Any, Callable, Dict, List, Union

from vcr import VCR, mode

from .patch import get_overridden_build


def scrub_header(unwanted_headers: List[str]) -> Callable:
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

            for unwanted_header in unwanted_headers:
                if unwanted_header in response["headers"]:
                    response["headers"].pop(unwanted_header)
        return response

    return before_record_response


default_vcr = VCR(
    path_transformer=VCR.ensure_suffix(".yaml"),
    filter_headers=[
        "User-Agent",
        "Accept",
        "Accept-Encoding",
        "Connection",
        "Content-Length",
        "Content-Type",
        # OpenAI request headers we don't want
        "Cookie",
        "authorization",
        "X-OpenAI-Client-User-Agent",
        "OpenAI-Organization",
        "x-stainless-lang",
        "x-stainless-package-version",
        "x-stainless-os",
        "x-stainless-arch",
        "x-stainless-runtime",
        "x-stainless-runtime-version",
    ],
    filter_query_parameters=["api_key"],
    before_record_response=scrub_header(
        [
            # OpenAI response headers we don't want
            "Set-Cookie",
            "Server",
            "access-control-allow-origin",
            "alt-svc",
            "openai-organization",
            "openai-version",
            "strict-transport-security",
            "x-ratelimit-limit-requests",
            "x-ratelimit-limit-tokens",
            "x-ratelimit-remaining-requests",
            "x-ratelimit-remaining-tokens",
            "x-ratelimit-reset-requests",
            "x-ratelimit-reset-tokens",
            "x-request-id",
        ]
    ),
    match_on=("method", "scheme", "host", "port", "path", "query", "body", "headers"),
    record_mode=mode.ONCE,
)

use_cassette = default_vcr.use_cassette


__all__ = [
    "get_overridden_build",
]

import itertools

import pytest

from vcr_langchain import matchers, request

# the dict contains requests with corresponding to its key difference
# with 'base' request.
REQUESTS = {
    "base": request.Request("Please respond", "FakeLLM"),
    "prompt": request.Request("Please don't respond", "FakeLLM"),
    "llm_string": request.Request("Please respond", "RealLLM"),
}


def assert_matcher(matcher_name):
    matcher = getattr(matchers, matcher_name)
    for k1, k2 in itertools.permutations(REQUESTS, 2):
        expecting_assertion_error = matcher_name in {k1, k2}
        if expecting_assertion_error:
            with pytest.raises(AssertionError):
                matcher(REQUESTS[k1], REQUESTS[k2])
        else:
            assert matcher(REQUESTS[k1], REQUESTS[k2]) is None


def test_matchers():
    assert_matcher("prompt")
    assert_matcher("llm_string")
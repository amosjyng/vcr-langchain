import itertools

import pytest

from vcr_langchain import matchers, request

# the dict contains requests with corresponding to its key difference
# with 'base' request.
REQUESTS = {
    "base": request.Request(prompt="Please respond", llm_string="FakeLLM"),
    "prompt": request.Request(prompt="Please don't respond", llm_string="FakeLLM"),
    "llm_string": request.Request(prompt="Please respond", llm_string="RealLLM"),
    "exact_base_copy": request.Request(prompt="Please respond", llm_string="FakeLLM"),
}


def assert_matcher(different_field):
    matcher = matchers.match_all
    for k1, k2 in itertools.permutations(REQUESTS, 2):
        expecting_assertion_error = "base" not in k1 or "base" not in k2
        if expecting_assertion_error:
            with pytest.raises(AssertionError):
                matcher(REQUESTS[k1], REQUESTS[k2])
        else:
            assert matcher(REQUESTS[k1], REQUESTS[k2]) is None


def test_matchers():
    assert_matcher("prompt")
    assert_matcher("llm_string")

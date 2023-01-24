from typing import List, Optional

import langchain
from langchain.llms.base import LLM

from tests import TemporaryCassettePath, vcr
from vcr_langchain import mode


class MockLLM(LLM):
    _NUM_CALLS = 0

    @property
    def _llm_type(self) -> str:
        return "MockLLM for testing"

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        MockLLM._NUM_CALLS += 1
        return (
            f"Wow, you really think you can ask me to '{prompt}'? "
            f"You've asked me to do this {MockLLM._NUM_CALLS} times."
        )


# pydantic requires _ in front of class variables, or else they won't exist
# make sure we set this successfully before continuing on with the rest of the test
assert MockLLM._NUM_CALLS == 0


def test_use_as_with_context():
    """This test doubles as a test for successful serialization"""
    cassette_path = "tests/context.yaml"
    with TemporaryCassettePath(cassette_path):
        with vcr.use_cassette(cassette_path, record_mode=mode.ONCE):
            llm = MockLLM()
            result = llm("Tell me a silly joke")

        with vcr.use_cassette(cassette_path, record_mode=mode.NONE):
            new_llm = MockLLM()
            assert new_llm("Tell me a silly joke") == result


def test_no_cache_outside_of_context():
    cassette_path = "tests/temp.yaml"
    assert langchain.llm_cache is None
    with TemporaryCassettePath(cassette_path):
        with vcr.use_cassette(cassette_path, record_mode=mode.ONCE):
            assert langchain.llm_cache is not None
            llm = MockLLM()
            llm("Tell me a temporary joke")

        assert langchain.llm_cache is None


def test_response_changes_without_context():
    llm = MockLLM()
    result = llm("Tell me a serious joke")

    new_llm = MockLLM()
    assert new_llm("Tell me a serious joke") != result


@vcr.use_cassette()
def test_use_as_test_decorator():
    llm = MockLLM()
    llm("Tell me a surreal joke")


@vcr.use_cassette("tests/custom.yaml")
def test_use_custom_file():
    llm = MockLLM()
    llm("Tell me a real joke")

import os
from typing import List, Optional

from langchain.llms.base import LLM

import vcr_langchain as vcr
from vcr_langchain import VCR, mode

my_vcr = VCR(path_transformer=VCR.ensure_suffix(".yaml"))


class MockLLM(LLM):
    @property
    def _llm_type(self) -> str:
        return "MockLLM for testing"

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        return f"Wow, you really think you can ask me to '{prompt}'?"


def test_use_as_with_context():
    cassette_path = "tests/context.yaml"
    if os.path.isfile(cassette_path):
        os.remove(cassette_path)
        assert not os.path.isfile(cassette_path)

    with vcr.use_cassette(cassette_path):
        llm = MockLLM()
        llm("Tell me a surreal joke")

    try:
        assert os.path.isfile(cassette_path)
    finally:
        os.remove(cassette_path)


@vcr.use_cassette(record_mode=mode.NONE)
def test_use_as_test_decorator():
    llm = MockLLM()
    llm("Tell me a surreal joke")


@vcr.use_cassette("tests/custom.yaml", record_mode=mode.NONE)
def test_use_custom_file():
    llm = MockLLM()
    llm("Tell me a surreal joke")

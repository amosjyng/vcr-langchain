import pytest
from langchain_openai import OpenAI

import vcr_langchain as vcr
from tests import TemporaryCassettePath


@pytest.mark.network
def test_use_as_with_context() -> None:
    """This test doubles as a test for successful serialization"""
    cassette_path = "tests/context.yaml"
    with TemporaryCassettePath(cassette_path):
        with vcr.use_cassette(cassette_path, record_mode=vcr.mode.ONCE):
            llm = OpenAI(model_name="text-ada-001")
            result = llm.invoke("Tell me a silly joke")

        with vcr.use_cassette(cassette_path, record_mode=vcr.mode.NONE):
            new_llm = OpenAI(model_name="text-ada-001")
            assert new_llm.invoke("Tell me a silly joke") == result


@vcr.use_cassette()
def test_use_as_test_decorator() -> None:
    llm = OpenAI(model_name="babbage-002")
    llm.invoke("Tell me a surreal joke")


@vcr.use_cassette("tests/custom.yaml")
def test_use_custom_file() -> None:
    llm = OpenAI(model_name="babbage-002")
    llm.invoke("Tell me a real joke")

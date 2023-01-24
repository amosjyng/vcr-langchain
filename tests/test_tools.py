import pytest
from langchain.serpapi import SerpAPIWrapper

from tests import vcr


@vcr.use_cassette()
def test_use_serp_api():
    answer = SerpAPIWrapper().run(query="how far is the moon receding every year")
    assert answer == "about 3.78 cm per year"


@pytest.mark.skip("Need to figure out positional variable hijack")
@vcr.use_cassette()
def test_use_serp_api_without_keyword():
    answer = SerpAPIWrapper().run("how far is the moon receding every year")
    assert answer == "about 3.78 cm per year"

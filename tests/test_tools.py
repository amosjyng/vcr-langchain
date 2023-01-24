from langchain.serpapi import SerpAPIWrapper

from tests import vcr


@vcr.use_cassette()
def test_use_serp_api():
    answer = SerpAPIWrapper().run(query="how far is the moon receding every year")
    assert answer == "about 3.78 cm per year"


@vcr.use_cassette()
def test_use_serp_api_without_keyword():
    answer = SerpAPIWrapper().run("how big is the sun")
    assert answer == "432,690 mi"

from langchain.python import PythonREPL
from langchain.serpapi import SerpAPIWrapper

from tests import TemporaryCassettePath, vcr


@vcr.use_cassette()
def test_use_serp_api():
    answer = SerpAPIWrapper().run(query="how far is the moon receding every year")
    assert answer == "about 3.78 cm per year"


@vcr.use_cassette()
def test_use_serp_api_without_keyword():
    answer = SerpAPIWrapper().run("how big is the sun")
    assert answer == "432,690 mi"


def test_use_python_repl():
    cassette_path = "python-with-keyword.yaml"
    with TemporaryCassettePath(cassette_path):
        with vcr.use_cassette(cassette_path):
            answer = PythonREPL().run(command="print(5 * 4)")
            assert answer.strip() == "20"


def test_use_python_repl_without_keyword():
    cassette_path = "python-no-keyword.yaml"
    with TemporaryCassettePath(cassette_path):
        with vcr.use_cassette(cassette_path):
            answer = PythonREPL().run("print(5 - 4)")
            assert answer.strip() == "1"


def test_use_python_repl_regularly():
    answer = PythonREPL().run("print(5 + 4)")
    assert answer.strip() == "9"

from langchain.python import PythonREPL
from langchain.serpapi import SerpAPIWrapper
from langchain.utilities.bash import BashProcess

import vcr_langchain as vcr
from tests import TemporaryCassettePath


@vcr.use_cassette()
def test_use_serp_api() -> None:
    answer = SerpAPIWrapper().run(query="how far is the moon receding every year")
    assert answer == "about 3.78 cm per year"


@vcr.use_cassette()
def test_use_serp_api_without_keyword() -> None:
    answer = SerpAPIWrapper().run("how big is the sun")
    assert answer == "432,690 mi"


def test_use_python_repl() -> None:
    cassette_path = "python-with-keyword.yaml"
    with TemporaryCassettePath(cassette_path):
        with vcr.use_cassette(cassette_path):
            answer = PythonREPL().run(command="print(5 * 4)")
            assert answer.strip() == "20"


def test_use_python_repl_without_keyword() -> None:
    cassette_path = "python-no-keyword.yaml"
    with TemporaryCassettePath(cassette_path):
        with vcr.use_cassette(cassette_path):
            answer = PythonREPL().run("print(5 - 4)")
            assert answer.strip() == "1"


def test_use_python_repl_regularly() -> None:
    answer = PythonREPL().run("print(5 + 4)")
    assert answer.strip() == "9"


@vcr.use_cassette()
def test_use_bash() -> None:
    time = BashProcess().run("date")
    assert time == "Fri Feb  3 13:05:45 +07 2023\n"


@vcr.use_cassette()
def test_use_bash_multiple_commands() -> None:
    test_filename = "tests/asdf"
    results = BashProcess().run(
        [
            f"touch {test_filename}",
            f"ls {test_filename}",
            f"rm {test_filename}",
        ]
    )
    assert results == "tests/asdf\n"


@vcr.use_cassette()
def test_use_bash_same_commands() -> None:
    test_filename = "tests/bsdf"
    bash = BashProcess()
    old_results = bash.run(f"ls {test_filename}")
    assert "returned non-zero exit status 2" in old_results
    bash.run(f"touch {test_filename}")
    new_results = bash.run(f"ls {test_filename}")
    assert new_results == "tests/bsdf\n"
    bash.run(f"rm {test_filename}")

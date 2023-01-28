import os
from typing import Any, List

from vcr_langchain import VCR, mode

vcr = VCR(
    path_transformer=VCR.ensure_suffix(".yaml"),
    record_mode=mode.ONCE,  # by default, make sure nothing is recorded
)


class TemporaryCassettePath:
    def __init__(self, cassette_path: str):
        self.cassette_path = cassette_path

    def __enter__(self) -> None:
        if os.path.isfile(self.cassette_path):
            os.remove(self.cassette_path)
            assert not os.path.isfile(self.cassette_path)

    def __exit__(self, *_: List[Any]) -> None:
        try:
            # check that cassette was successfully created
            assert os.path.isfile(self.cassette_path)
        finally:
            # remove it for future testing
            os.remove(self.cassette_path)

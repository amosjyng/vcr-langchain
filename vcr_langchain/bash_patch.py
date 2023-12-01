from typing import Any, Callable, Dict, List, Union, cast

from langchain_experimental.llm_bash.base import BashProcess
from vcr.cassette import Cassette

from .generic import GenericPatch


class BashProcessPatch(GenericPatch):
    def __init__(self, cassette: Cassette):
        super().__init__(cassette, BashProcess, "run")

    def get_meta_information(self, og_self: Any) -> Dict[str, Any]:
        bash_process = cast(BashProcess, og_self)
        return {
            "persistent": bash_process.process is not None,
            "strip_newlines": bash_process.strip_newlines,
            "return_err_output": bash_process.return_err_output,
        }

    def get_same_signature_override(self) -> Callable:
        def run(og_self: BashProcess, commands: Union[str, List[str]]) -> str:
            """Same signature override patched into BashProcess"""
            return self.generic_override(og_self, commands=commands)

        return run

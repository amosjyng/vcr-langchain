from copy import deepcopy
from dataclasses import dataclass

from vcr.request import Request as OgRequest


@dataclass
class Request:
    """A request to an LLM or a tool"""

    def __init__(self, **kwargs) -> None:
        """
        Only keyword arguments allowed. You should write a wrapper function that takes
        in args if the original callsite takes args, and convert them into kwargs.
        This way, it's always clear what the request is for.
        """
        self.kwargs = kwargs

    def args(self):
        return sorted(self.kwargs.keys())

    def _to_dict(self):
        args = deepcopy(self.kwargs)
        if "prompt" in args:
            # str the prompt up in case it's a fancy subclass of str -- e.g. Fvalues
            args["prompt"] = str(self.kwargs["prompt"])
        return args

    @classmethod
    def _from_dict(cls, dct):
        return Request(**dct)


# hijack the other _from_dict method
OgRequest._from_dict = Request._from_dict

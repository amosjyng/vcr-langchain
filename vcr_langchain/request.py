from dataclasses import dataclass

from vcr.request import Request as OgRequest


@dataclass
class Request:
    """A request to an LLM"""

    # Prompt sent to the LLM
    prompt: str
    # LLM descriptor
    llm_string: str

    def _to_dict(self):
        return {
            # str the prompt up in case it's a fancy subclass of str -- e.g. Fvalues
            "prompt": str(self.prompt),
            "llm_string": self.llm_string,
        }

    @classmethod
    def _from_dict(cls, dct):
        return Request(**dct)


# hijack the other _from_dict method
OgRequest._from_dict = Request._from_dict

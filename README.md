# VCR langchain

Adapts [VCR.py](https://github.com/kevin1024/vcrpy) for use with [langchain](https://github.com/hwchase17/langchain) so that you can record and replay all your expensive LLM interactions for tests.

## Quickstart

```bash
pip install vcr-langchain
```

Use it with pytest:

```python
import vcr_langchain as vcr
from langchain.llms import OpenAI

@vcr.use_cassette()
def test_use_as_test_decorator():
    llm = OpenAI(model_name="text-ada-001")
    assert llm("Tell me a surreal joke") == "<put the output here>"
```

The next time you run it:

- the output is now deterministic
- it executes a lot faster by replaying from cache
- you no longer need to have the real OpenAI API key defined

For more examples, see [the usages test file](tests/test_usage.py).

### Why not just use VCR.py directly?

This offers higher-level, more human-readable recordings for inspection. Additionally, I plan to support recording of utilities as well, which includes non-network requests such as command executions inside Bash or the Python REPL.

## Documentation

For more information on how VCR works and what other options there are, please see the [VCR docs](https://vcrpy.readthedocs.io/en/latest/index.html).

For more information on how to use langchain, please see the [langchain docs](https://langchain.readthedocs.io/en/latest/).

# VCR LangChain

Patches [VCR.py](https://github.com/kevin1024/vcrpy) to include non-network tooling for use with [LangChain](https://github.com/hwchase17/langchain). Refactor with confidence as you record and replay all your LLM logic in a contained environment, free from any and all side effects.

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
- no command executions or other side effects actually happen
- you no longer need to have real API keys defined for test execution in CI environments

For more examples, see [the usages test file](tests/test_usage.py).

If you're using the Langchain Playwright browser tools, you can also use [`get_sync_test_browser` and `get_async_test_browser`](/vcr_langchain/dummy.py) to automatically get real browsers during recording but fake browsers on replay. This allows you to skip downloading and installing Playwright browsers on your remote CI server, while still being able to re-record sessions in a real browser when developing locally.

### Pitfalls

Note that tools, if initialized outside of the `vcr_langchain` decorator, will not have recording capabilities patched in. This is true even if an agent using those tools is initialized within the decorator.

## Documentation

For more information on how VCR works and what other options there are, please see the [VCR docs](https://vcrpy.readthedocs.io/en/latest/index.html).

For more information on how to use langchain, please see the [langchain docs](https://langchain.readthedocs.io/en/latest/).

**Please note that there is a lot of langchain functionality that I haven't gotten around to hijacking for recording.** If there's anything you need to record in a cassette, please open a PR or issue.

## Projects that use this

- [LangChain Visualizer](https://github.com/amosjyng/langchain-visualizer)

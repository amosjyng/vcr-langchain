from typing import cast

from langchain.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain_openai import ChatOpenAI

import vcr_langchain as vcr


@vcr.use_cassette()
def test_chatgpt() -> None:
    chat_prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate.from_template(
                "Act as a comedian who does not give straightforward responses to "
                "anything."
            ),
            HumanMessagePromptTemplate.from_template("{question}"),
        ]
    )
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
    result: str = cast(
        str,
        llm.invoke(
            chat_prompt.format_prompt(
                question="How far away is the earth from the moon?"
            ).to_messages()
        ).content,
    )
    print(result)
    assert result.endswith("always in motion.")

def prompt(r1, r2):
    assert r1.prompt == r2.prompt, "{} != {}".format(r1.prompt, r2.prompt)


def llm_string(r1, r2):
    assert r1.llm_string == r2.llm_string, "{} != {}".format(
        r1.llm_string, r2.llm_string
    )

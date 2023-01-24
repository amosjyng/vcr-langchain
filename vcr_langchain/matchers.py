from vcr_langchain.request import Request


def match_args(r1: Request, r2: Request):
    r1_args = r1.args()
    r2_args = r2.args()
    assert r1_args == r2_args, "Arguments differ: {} != {}".format(r1_args, r2_args)


def match_field(r1: Request, r2: Request, field_name: str):
    r1_value = r1.kwargs[field_name]
    r2_value = r2.kwargs[field_name]
    assert r1_value == r2_value, "{} != {}".format(r1_value, r2_value)


def match_all(r1: Request, r2: Request):
    match_args(r1, r2)
    for arg in r1.args():
        match_field(r1, r2, arg)

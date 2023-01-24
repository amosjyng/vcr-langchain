from vcr_langchain import VCR, mode

vcr = VCR(
    path_transformer=VCR.ensure_suffix(".yaml"),
    record_mode=mode.ONCE,  # by default, make sure nothing is recorded
)

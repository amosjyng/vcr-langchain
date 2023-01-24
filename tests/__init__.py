from vcr_langchain import VCR, mode

vcr = VCR(
    path_transformer=VCR.ensure_suffix(".yaml"),
    record_mode=mode.NONE,  # by default, make sure nothing is recorded
)

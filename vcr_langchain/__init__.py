from vcr import mode as og_mode

from .config import VCR

default_vcr = VCR()
use_cassette = default_vcr.use_cassette
mode = og_mode

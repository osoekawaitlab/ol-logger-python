import re

import ollogger


def test_ollogger_has_version() -> None:
    assert re.match(r"\d+\.\d+\.\d+", ollogger.__version__)

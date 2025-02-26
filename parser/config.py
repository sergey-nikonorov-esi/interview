import os
from pathlib import Path

import tests

#-------------------------------------------------------------------------

DATA_DIR = Path(os.path.realpath('.')) / 'data'

#-------------------------------------------------------------------------
## test runner wrapper

def run_tests(parser):

    tests.run \
    (
        test_kwargs = dict \
        (
            raw_dir = DATA_DIR / 'raw',
            parsed_dir = DATA_DIR / 'parsed',
            parser = parser
        )
    )

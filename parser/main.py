from pathlib import Path

import re
import pandas as pd

import config
import tests

#-------------------------------------------------------------------------
## helpers (you may want to modify/use those as a base);
## you may also want to check the `utils.py` file in this repository

INTEGER = r'(?:[\-+]?\d+)'
FLOAT = rf'(?:[\-+]?\d*(?:\d\.|\.\d)\d*(?:[eE]{INTEGER})?)'
NUMBER = rf'(?:{FLOAT}|{INTEGER})'

SP = r'[ \t]*'

ARROW = rf'<?-*(?:-\[{SP}{NUMBER}{SP}\]-|-)-*>?'
"""
this will match any `arrow` (as defined in the Format Specification)
"""

#-------------------------------------------------------------------------

def parse(path: Path | str) -> pd.DataFrame:
	...

#-------------------------------------------------------------------------
## testing the parser

tests.run \
(
	test_kwargs = dict \
	(
		raw_dir = config.DATA_DIR / 'raw',
		parsed_dir = config.DATA_DIR / 'parsed',
		parser = parse
	)
)

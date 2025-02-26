import os
import sys

from pathlib import Path

from dataclasses import dataclass
from typing import Callable, Union

import pandas as pd

from unittest import TestCase, TestSuite, TextTestRunner

#-------------------------------------------------------------------------

@dataclass
class DataFrameTest(TestCase):

    raw:    pd.DataFrame
    parsed: pd.DataFrame

    def __post_init__(self):
        super().__init__('test')

    def test(self):
        self.assertTrue \
        (
            self.raw.equals(self.parsed),
            msg = f"\n\nexpected:\n{self.parsed}\n\ngot:\n{self.raw}"
        )

#-------------------------------------------------------------------------

def _collect_ext(names) -> dict:

    res = {}
    for basename, ext in map(os.path.splitext, names):
        res.setdefault(basename, []).append(ext)

    if not all(len(v) == 1 for v in res.values()):
        raise ValueError(f"the `{{basename: extension}}` mapping is not injective:\n{res}")

    return \
    {
        key: value[0]
        for key, value in res.items()
    }

def make_tests \
(
    raw_dir:    Union[Path, str],
    parsed_dir: Union[Path, str],
    parser:     Callable[[Union[Path, str]], pd.DataFrame]
):

    raw_dir = Path(raw_dir)
    parsed_dir = Path(parsed_dir)

    raw_names = os.listdir(raw_dir)
    parsed_names = os.listdir(parsed_dir)

    raw_ext = _collect_ext(raw_names)
    parsed_ext = _collect_ext(parsed_names)

    matching = sorted(raw_ext.keys() & parsed_ext.keys())

    all_tests = TestSuite()

    for basename in matching:

        cls = type \
        (
            f'[{basename}]',
            (DataFrameTest,),
            {}
        )

        test = cls \
        (
            parser(raw_dir / f'{basename}{raw_ext[basename]}'),
            pd.read_csv(parsed_dir / f'{basename}{parsed_ext[basename]}')
        )

        all_tests.addTest(test)

    print('-'*60)

    return all_tests

#-------------------------------------------------------------------------

def run(test_kwargs, runner_kwargs = None):

    runner_kwargs = runner_kwargs or {}
    runner_kwargs.setdefault('verbosity', 2)
    runner_kwargs.setdefault('stream', sys.stdout)

    all_tests = make_tests(**test_kwargs)
    runner = TextTestRunner(**runner_kwargs)

    runner.run(all_tests)

from dataclasses import dataclass
from os.path import splitext
from typing import Any, Iterable, Optional, Union

#-------------------------------------------------------------------------

def strided(arr, chunk_size, step):
    """
    returns a generator of strided chunks from `arr`
    
    examples:
        >>> [*strided('ABCDE', 3, 1)]
        ['ABC', 'BCD', 'CDE']
        >>> [*strided('AB--CD--EF-', 2, 4)]
        ['AB', 'CD', 'EF']
        >>> [*strided('A.B C.D  ', 3, 4)]
        ['A.B', 'C.D']
    """
    return \
    (
        arr[idx:idx + chunk_size]
        for idx in range(0, len(arr) - chunk_size + 1, step)
    )

def joined(values: Iterable[Iterable]):
    """
    concatenates iterables from `values`
    
    examples:
        >>> joined([(1, 2), ('#', None, -1)])
        [1, 2, '#', None, -1]
        >>> joined([range(2), range(3)])
        [0, 1, 0, 1, 2]
    """
    res = []
    for v in values:
        res.extend(v)
    return res

#-------------------------------------------------------------------------

@dataclass
class ConstantMapping:

    value:   Any
    support: Optional[set] = None

    def __post_init__(self):
        if self.support is not None and not isinstance(self.support, set):
            self.support = set(self.support)

    def __getitem__(self, key, default = None):
        if self.support is None or key in self.support:
            return self.value
        else:
            return default

    def keys(self):
        return self.support

def collect_ext(names, injective = True) -> Union[dict, ConstantMapping]:

    res = {}
    for basename, ext in map(splitext, names):
        res.setdefault(basename, []).append(ext)

    if injective:
        for key, value in res.items():
            if len(value) > 1:
                raise ValueError \
                (
                  f'base name {key!r} corresponds to several extensions: {value}'
                )

        res = \
        {
            key: value[0]
            for key, value in res.items()
        }

        all_values = set(res.values())

        if len(all_values) == 1:
            res = ConstantMapping \
            (
                value = next(iter(all_values)),
                support = res.keys()
            )

    return res
    
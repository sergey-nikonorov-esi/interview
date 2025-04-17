from typing import Collection

#-------------------------------------------------------------------------

def dot_apply(*F):
    """
    reverse function composition, i.e.:
       `dot_apply(f1, f2, f3) == x -> f3(f2(f1(x)))`

    the name comes from the fact that the result resembles a chain method call:
       `x -> x.f1().f2().f3()`
    """

    def __f(x):
        for f in F:
            x = f(x)
        return x

    return __f

def strided(arr: Collection, chunk_size, step):
    """
    returns a generator of strided chunks from `arr`

    Examples:

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

def collection_like(a) -> bool:

    try:
        if isinstance(a, (str, bytes)):
            raise TypeError

        iter(a)
        return True

    except TypeError:
        return False

def flatten(a, *, is_collection = collection_like):
    """
    yields elements from `a` recursively, effectively implementing a flat iterator

    **kwargs:
        is_collection: Predicate (default: collection_like)
            a predicate that defines which objects should be treated as collections
            (can be used to prevent the flattening of certain iterables, see examples below)

    Examples:

    >>> [*flatten([1, [2, 3, [[4], 5]]])]
    [1, 2, 3, 4, 5]

    >>> [*flatten([1, (0.5, -1), [[2, 3]]])]
    [1, 0.5, -1, 2, 3]

    >>> is_collection = lambda obj: collection_like(obj) and not isinstance(obj, tuple)
    >>> [*flatten([1, (0.5, -1), [[2, 3]]], is_collection = is_collection)]
    [1, (0.5, -1), 2, 3]
    """

    if is_collection(a):
        for v in a:
            yield from flatten(v, is_collection = is_collection)
    else:
        yield a

import itertools
from typing import List, cast


def product_list(*iterables, repeat=1, out=None):
    'same as itertools.product, but mutates the output instead of making tuples'
    dims = [list(it) for it in iterables] * repeat
    n = len(dims)
    if out is not None:
        assert len(out) == n, f'Incompatible output shape'
    out = [None] * n if out is None else out

    def backtrack(i):
        if i == n:
            yield out
        else:
            for x in dims[i]:
                out[i] = x
                yield from backtrack(i + 1)

    yield from backtrack(0)
    return


def isomorphism_candidates(hashesA: List[int], hashesB: List[int], out=None):
    '''
    Yields all injective and surjective mappings
        f from range(n) to range(n)
    such that
        all(hashesA[i] == hashesB[f[i]] for i in range(n))
    where n = len(hashesA) = len(hashesB).
    '''
    n = len(hashesA)
    if len(hashesB) != n:
        return

    if out is not None:
        assert len(out) == n, f'Incompatible output shape'

    out = [None] * n if out is None else out
    out = cast(List[int], out)

    if sorted(hashesA) != sorted(hashesB):
        return

    groups = {v: ([], []) for v in [*hashesA, *hashesB]}
    for i, v in enumerate(hashesA):
        groups[v][0].append(i)
    for i, v in enumerate(hashesB):
        groups[v][1].append(i)
    groups = [*groups.values()]
    for idxA, idxB in groups:
        if len(idxA) != len(idxB):
            return

    m = len(groups)

    def backtrack(group_i):
        if group_i == m:
            yield out
        else:
            gA, gB = groups[group_i]
            for gBperm in itertools.permutations(gB):
                for i, j in zip(gA, gBperm):
                    out[i] = j
                yield from backtrack(group_i + 1)

    yield from backtrack(0)
    return

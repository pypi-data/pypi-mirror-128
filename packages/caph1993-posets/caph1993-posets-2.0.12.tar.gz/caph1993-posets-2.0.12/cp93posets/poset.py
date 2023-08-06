from __future__ import annotations
from typing import Iterable, List, Optional, Sequence, Set, Tuple
from cp93pytools.methodtools import cached_property
from .poset_exceptions import (
    NotUniqueBottomException,
    PosetExceptions,
    NotLatticeException,
)
from .help_index import HelpIndex
from .poset_wbools import WBools
from .algorithm_random_poset_czech import random_lattice as random_lattice_czech
import pyhash
import numpy as np
from collections import deque
from itertools import product, chain
from functools import reduce
import time, sys
import re

npBoolMatrix = np.ndarray
npUInt64Matrix = np.ndarray


class Relation(HelpIndex, WBools):
    '''
    Class for boolean relation matrices intended mostly for asserting that
    a matrix relation can be used with the fully featured Poset class.
    '''

    def __init__(self, rel: npBoolMatrix):
        shape = tuple(rel.shape)
        assert len(shape) == 2, f'{shape}? matrix must be 2-dimensional'
        n = shape[0]
        assert shape == (n, n), f'{shape}? matrix must be squared'
        assert rel.dtype == bool, 'matrix must be a boolean numpy array'
        assert rel.flags.writeable == False, 'matrix must be read-only'
        self.n = rel.shape[0]
        self.rel = rel
        return

    '''
    @section
        Display methods
    '''

    def describe(self):
        self.show()
        print('Relation matrix:')
        print(self.rel.astype(int))
        print('Reflexive?', self.is_reflexive)
        print('Antisymmetric?', self.is_antisymmetric)
        print('Transitive?', self.is_transitive)
        return

    def show(self, labels=None, save=None):
        'Display the relation using graphviz. Groups SCCs together'
        scc_components, scc_edges = self.scc_reduction()
        if labels is None:
            labels = [f'{i}' for i in range(self.n)]
        n = len(scc_components)
        labels = ['-'.join(labels[i] for i in I) for I in scc_components]
        return graphviz(n, edges=scc_edges, labels=labels, save=save)

    '''
    @section
        Validation and boolean property methods
    '''

    @cached_property
    def is_poset(self):
        return (self.is_reflexive and self.is_antisymmetric and
                self.is_transitive)

    @cached_property
    def is_reflexive(self):
        rel = self.rel
        I, = np.where(~rel[np.diag_indices_from(rel)])
        why = I.size and f'Not reflexive: rel[{I[0]},{I[0]}] is False'
        return self._wbool(not why, why)

    @cached_property
    def is_antisymmetric(self):
        rel = self.rel
        eye = np.identity(self.n, dtype=np.bool_)
        I, J = np.where(rel & rel.T & ~eye)
        why = I.size and f'Not antisymmetric: cycle {I[0]}<={I[1]}<={I[0]}'
        return self._wbool(not why, why)

    @cached_property
    def is_transitive(self):
        rel = self.rel
        rel2 = np.matmul(rel, rel)
        I, J = np.where(((~rel) & rel2))
        why = I.size and (
            f'Not transitive: rel[{I[0]},{J[0]}] is False but there is a path')
        return self._wbool(not why, why)

    @classmethod
    def validate(cls, rel: npBoolMatrix, expect_poset: bool = False):
        instance = cls(rel)
        if expect_poset:
            instance.is_poset.assert_explain()
        return instance

    '''
    @section
        Graph operations
    '''

    def scc_reduction(self):
        n = self.n
        rel = self.rel
        G = [[] for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if rel[i, j] and i != j:
                    G[i].append(j)
        return Tarjan(G).tarjan()

    def transitive_closure(self):
        if self.is_transitive:
            return self
        dist = floyd_warshall(self.rel, infinity=self.n)
        rel = (dist < len(dist))
        rel.flags.writeable = False
        return self.__class__(rel)

    def transitive_reduction(self, _assume_poset=False):
        ''''
        Compute the transitive reduction of the given relation
        Raises an exception if the relation is not a poset
        The output relation is also known as "Hasse diagram"
        '''
        if not _assume_poset:
            self.is_poset.assert_explain()
        lt = self.rel.copy()
        lt[np.diag_indices_from(lt)] = False
        any_inbetween = np.matmul(lt, lt)
        child = lt & ~any_inbetween
        child.flags.writeable = False
        return self.__class__(child)


class Poset(HelpIndex, WBools):
    '''
    Hashable object that represents an inmutable finite partial order.
    Uses a matrix and hashing is invariant under permutations.

    The main attributes (always present) are:
        - n: size of the poset. The elements of the poset are range(n)
        - leq: read only less-or-equal boolean nxn matrix:
            leq[i,j]==True iff i <= j
        - labels: tuple of n strings. Only used for displaying
    '''

    def __init__(self, leq: npBoolMatrix, labels: Sequence[str] = None,
                 _validate=False):
        'Assumes that leq is indeed a valid poset relation'
        Relation.validate(leq, expect_poset=_validate)
        self.n = n = leq.shape[0]
        self.leq = leq
        if labels is not None:
            m = len(labels)
            assert m == n, f'{m} labels found. Expected {n}'
            non = [l for l in labels if not isinstance(l, str)]
            assert not non, f'non-string label found: {non[0]}'
        self._labels = labels

    @cached_property
    def labels(self):
        return self._labels or tuple(f'{i}' for i in range(self.n))

    '''
    @section
        Display methods
    '''

    def describe(self):
        self.show()
        print('Relation matrix:')
        print(self.leq.astype(int))
        print('Covers:', self)
        print(f'Lattice? {self.is_lattice}')
        if self.is_lattice:
            print(f'Distributive? {self.is_distributive}')
        else:
            print(f'# bottoms: {len(self.bottoms)}')
            print(f'# tops: {len(self.tops)}')
        return

    @cached_property
    def name(self):
        'Compact and readable representation of self based on parents'
        n = self.n
        P = self.parents
        topo = self.toposort
        Pstr = lambda i: ','.join(map(str, P[i]))
        it = (f'{i}<{Pstr(i)}' for i in topo if P[i])
        name = ' : '.join((f'{n}', *it))
        labels = ''
        if self.labels != tuple(range(n)):
            labels = ', '.join(self.labels)
            labels = f' with labels {labels}'
        return f'P({name}){labels}'

    def __repr__(self):
        return self.name

    def show(self, f=None, method='auto', labels=None, save=None):
        '''
        Use graphviz to display or save self as a Hasse diagram.
        The argument "method" (string) only affects visualization
        of the endomorphism f (if given). It can be
          - arrows: blue arrow from each node i to f[i]
          - labels: replace the label i of each node with f[i]
          - labels_bottom: (no label at i if f[i]=bottom)
          - arrows_bottom: (no arrow at i if f[i]=bottom)
          - auto: 'arrows_bottom' if self is a lattice and f preserves lub. 'arrows' otherwise.
        Hidding bottom is only allowed if self.bottom makes sense.
        '''

        methods = ('auto', 'labels', 'arrows', 'labels_bottom', 'arrows_bottom')
        assert method in methods, f'Unknown method "{method}"'

        if method == 'auto' and f is not None:
            if self.is_lattice and self.f_is_lub(f):
                method = 'arrows_bottom'
            else:
                method = 'arrows'
        n = self.n
        child = self.child
        blue_edges = None
        if labels is None:
            labels = self.labels
        if f is not None:
            enabled = not method.endswith('_bottom')
            ok = lambda fi: enabled or fi != self.bottom
            if method.startswith('arrows'):
                blue_edges = [(i, int(f[i])) for i in range(n) if ok(f[i])]
            else:
                gr = [[] for _ in range(n)]
                for i in range(n):
                    if ok(f[i]):
                        gr[f[i]].append(i)
                labels = [','.join(map(str, l)) for l in gr]

        edges = [(i, j) for i in range(n) for j in range(n) if child[i, j]]
        graphviz(n, edges, labels=labels, blue_edges=blue_edges, save=save)

    '''
    @section
        Cover relation methods 
    '''

    @cached_property
    def child(self):
        '''
        nxn boolean matrix: transitive reduction of the poset.
        child[i,j]==True iff j covers i (with no elements inbetween)
        '''
        red = Relation(self.leq).transitive_reduction(_assume_poset=True)
        return red.rel

    @cached_property
    def children(self):
        ''' top-down adjoint list (j in G[i] iff i covers j)'''
        n = self.n
        child = self.child
        return [[j for j in range(n) if child[j, i]] for i in range(n)]

    @cached_property
    def parents(self):
        '''bottom-up adjoint list (j in G[i] iff j covers i)'''
        n = self.n
        child = self.child
        return [[j for j in range(n) if child[i, j]] for i in range(n)]

    '''
    @section
        Interface methods
    '''

    @classmethod
    def from_parents(cls, parents, labels=None):
        'create Poset from list: parents[i] = list of parents of i'
        n = len(parents)
        children = [[] for _ in range(n)]
        for ch in range(n):
            for pa in parents[ch]:
                children[pa].append(ch)
        return cls.from_children(children, labels)

    @classmethod
    def from_children(cls, children, labels=None):
        'create Poset from list: children[i] = list of covers of i'
        n = len(children)
        child = np.zeros((n, n), dtype=bool)
        for pa in range(n):
            for ch in children[pa]:
                child[ch, pa] = True
        child.flags.writeable = False
        dist = cls.child_to_dist(child, assume_poset=False)
        dist.flags.writeable = False
        leq = dist < n
        leq.flags.writeable = False
        poset = cls(leq, labels, _validate=True)
        poset.__dict__['child'] = child
        poset.__dict__['dist'] = dist
        return poset

    @classmethod
    def from_down_edges(cls, n, edges):
        'create Poset of size n respecting all given relations (ancestor, descendant)'
        return cls.from_up_edges(n, [(j, i) for i, j in edges])

    @classmethod
    def from_up_edges(cls, n, edges):
        'create Poset of size n respecting all given relations (descendant, ancestor)'
        leq = np.zeros((n, n), dtype=bool)
        leq[np.diag_indices_from(leq)] = True
        for des, anc in edges:
            leq[des, anc] = True
        leq.flags.writeable = False
        closure = Relation(leq).transitive_closure()
        return cls(closure.rel, _validate=True)

    @classmethod
    def from_lambda(cls, elems, f_leq, labels=None):
        'create Poset with: leq[i,j] = f_leq(elems[i], elems[j])'
        m = len(elems)
        leq = np.zeros((m, m), dtype=bool)
        for i in range(m):
            for j in range(m):
                leq[i, j] = f_leq(elems[i], elems[j])
        leq.flags.writeable = False
        return cls(leq, labels, _validate=True)

    @cached_property
    def heights(self):
        'Array of distance from i down to any bottom'
        dist = self.dist
        bottoms = self.bottoms
        return tuple(np.min([dist[i, :] for i in bottoms], axis=0))

    @cached_property
    def dist(self):
        'Matrix of shortest distance from i upwards to j through child'
        return self.__class__.child_to_dist(self.child, assume_poset=True)

    @classmethod
    def child_to_dist(cls, child: npBoolMatrix, assume_poset=False):
        'Compute all pairs shortest distances using Floyd-Warshall algorithm'
        # To do: use toposort or repeated dijsktra if assume_poset==True
        dist = floyd_warshall(child, infinity=child.shape[0])
        dist.flags.writeable = False
        return dist

    '''
    @section
        Graph structure methods
    '''

    def _parse_domain(self, domain: List[int] | List[bool]) -> List[int]:
        n = self.n
        assert len(domain) <= n, f'Invalid domain: {domain}'
        if len(domain) == n > 0:
            if isinstance(domain[0], bool):
                domain = [i for i in range(n) if domain[i]]
        else:
            assert len(set(domain)) == len(domain), f'Invalid domain: {domain}'
        return domain  # type:ignore

    def subgraph(self, domain: List[int] | List[bool]):
        domain = self._parse_domain(domain)
        m = len(domain)
        leq = self.leq
        sub = np.zeros((m, m), dtype=bool)
        for i in range(m):
            for j in range(m):
                sub[i, j] = leq[domain[i], domain[j]]
        sub.flags.writeable = False
        labels = tuple(self.labels[i] for i in domain)
        return self.__class__(sub, labels=labels)

    @cached_property
    def toposort(self):
        n = self.n
        G = self.parents
        child = self.child
        indeg = [child[:, i].sum() for i in range(n)]
        topo = []
        q = deque([i for i in range(n) if indeg[i] == 0])
        while q:
            u = q.popleft()
            topo.append(u)
            for v in G[u]:
                indeg[v] -= 1
                if indeg[v] == 0:
                    q.append(v)
        assert len(topo) == n, f'Not antisymmetric, cycle found'
        return tuple(topo)

    @cached_property
    def toporank(self):
        return tuple(self.__class__.inverse_permutation(self.toposort))

    @classmethod
    def inverse_permutation(cls, perm: Sequence[int]):
        n = len(perm)
        rank = [-1] * n
        for i in range(n):
            rank[perm[i]] = i
        return rank

    @cached_property
    def independent_components(self):
        'Graph components if all edges were bidirectional'
        n = self.n
        cmp = self.leq | self.leq.T
        G = [[j for j in range(n) if cmp[i, j]] for i in range(n)]
        color = np.ones(n, dtype=int) * -1

        def component(i):
            q = deque([i])
            found = []
            while q:
                u = q.popleft()
                for v in G[u]:
                    if color[v] != color[u]:
                        color[v] = color[u]
                        q.append(v)
                found.append(u)
            return found

        comps = []
        for i in range(n):
            if color[i] == -1:
                color[i] = len(comps)
                comps.append(component(i))
        return comps

    '''
    @section
        Lattice methods
    '''

    def assert_lattice(self):
        self.is_lattice.assert_explain()

    @cached_property
    def is_lattice(self):
        try:
            if self.n > 0:
                self.lub
                self.bottom
        except NotUniqueBottomException as e:
            reason = f"Not unique bottom: {self.bottoms}"
            return self._wbool(False, reason)
        except NotLatticeException as e:
            i, j = e.args
        else:
            return self._wbool(True)
        n = self.n
        leq = self.leq
        above = [k for k in range(n) if leq[i, k] and leq[j, k]]
        below = [k for k in range(n) if leq[k, i] and leq[k, j]]
        if not above:
            reason = f'Not a lattice: {i} lub {j} => (no common ancestor)'
            return self._wbool(False, reason)
        if not below:
            reason = f'Not a lattice: {i} glb {j} => (no common descendant)'
            return self._wbool(False, reason)
        lub = min(above, key=lambda k: sum(leq[:, k]))
        glb = max(below, key=lambda k: sum(leq[:, k]))
        for x in above:
            if not leq[lub, x]:
                reason = f'Not a lattice: {i} lub {j} => {lub} or {x}'
                return self._wbool(False, reason)
        for x in below:
            if not leq[x, glb]:
                reason = f'Not a lattice: {i} glb {j} => {glb} or {x}'
                return self._wbool(False, reason)
        return self._wbool(False, 'Unknown reason')

    @cached_property
    def lub(self):
        'matrix of i lub j, i.e. i join j'
        n = self.n
        leq = self.leq
        lub_id = {tuple(leq[i, :]): i for i in range(n)}
        lub = np.zeros((n, n), int)
        for i in range(n):
            for j in range(n):
                above = tuple(leq[i, :] & leq[j, :])
                if above not in lub_id:
                    self._lub_issue = (i, j)
                    raise NotLatticeException(args=(i, j))
                lub[i, j] = lub_id[above]
        lub.flags.writeable = False
        return lub

    @cached_property
    def bottoms(self):
        'bottom elements of the poset'
        n = self.n
        nleq = self.leq.sum(axis=0)
        return [i for i in range(n) if nleq[i] == 1]

    @cached_property
    def non_bottoms(self):
        'non-bottom elements of the poset'
        n = self.n
        nleq = self.leq.sum(axis=0)
        return [i for i in range(n) if nleq[i] > 1]

    @cached_property
    def tops(self):
        'top elements of the poset'
        n = self.n
        nleq = self.leq.sum(axis=0)
        return [i for i in range(n) if nleq[i] == n]

    @cached_property
    def non_tops(self):
        'non-top elements of the poset'
        n = self.n
        nleq = self.leq.sum(axis=0)
        return [i for i in range(n) if nleq[i] < n]

    # @cached_property
    # def has_unique_bottom(self):
    #     unique = len(self.bottoms) == 1
    #     reason = not unique and f'Multiple bottoms: {self.bottoms}'
    #     return self._wbool(unique, reason)

    @cached_property
    def bottom(self):
        'unique bottom element of the Poset. Throws if not present'
        bottoms = self.bottoms
        if not bottoms:
            raise PosetExceptions.NoBottomsException()
        if len(bottoms) > 1:
            hook = lambda: f'Multiple bottoms found: {bottoms}'
            raise PosetExceptions.NotUniqueBottomException(hook)
        return bottoms[0]

    @cached_property
    def top(self):
        'unique top element of the Poset. Throws if not present'
        tops = self.tops
        if not tops:
            raise PosetExceptions.NoTopsException()
        if len(tops) > 1:
            hook = lambda: f'Multiple tops found: {tops}'
            raise PosetExceptions.NotUniqueTopException(hook)
        return tops[0]

    @cached_property
    def irreducibles(self):
        n = self.n
        children = self.children
        return [i for i in range(n) if len(children[i]) == 1]

    @cached_property
    def glb(self):
        geq = self.leq.T
        return self.__class__(geq).lub

    '''
    @section
        Hashing and isomorphisms
    '''

    _hasher = pyhash.xx_64(seed=0)

    @classmethod
    def hasher(cls, ints):
        'Fast hash that is consistent across runs independently of PYTHONHASHSEED'
        return cls._hasher(
            str(ints)[1:-1]) >> 1  # Prevent uint64->int64 overflow

    def hash_perm_invariant(self, mat):
        HASH = self.__class__.hasher
        h = lambda l: HASH(sorted(l))
        a = [HASH((h(mat[:, i]), h(mat[i, :]))) for i in range(self.n)]
        return np.array(a, dtype=int)

    @cached_property
    def hash_elems(self):
        mat = self.leq.astype(np.int64)
        with np.errstate(over='ignore'):
            H = self.hash_perm_invariant(mat)
            for repeat in range(2):
                mat += np.matmul(H[:, None], H[None, :])
                H = self.hash_perm_invariant(mat)
        return H

    @cached_property
    def hash(self):
        return self.__class__.hasher(sorted(self.hash_elems))

    def __hash__(self):
        return self.hash

    def __eq__(self, other):
        'Equality up to isomorphism, i.e. up to reindexing'
        N_NO_HASH_COLLISIONS_TESTED = 10
        if self.n == other.n <= N_NO_HASH_COLLISIONS_TESTED:
            eq = hash(self) == hash(other)
        else:
            eq = self.find_isomorphism(other) is not None
        return eq

    def find_isomorphism(self, other):
        # Quick check:
        if self.n != other.n or hash(self) != hash(other):
            return None

        # Filter out some functions:
        n = self.n
        Ah = self.hash_elems
        Bh = other.hash_elems

        matches = [[j for j in range(n) if Ah[i] == Bh[j]] for i in range(n)]
        remaining = product_list(*matches)

        # Find isomorphism among remaining functions
        A = self.leq
        B = other.leq

        def is_isomorphism(f):
            return all(
                A[i, j] == B[f[i], f[j]] for i in range(n) for j in range(n))

        return next((f for f in remaining if is_isomorphism(f)), None)

    def reindex(self, f, inverse=False, reset_labels=False):
        'Reindexed copy of self such that i is to self as f[i] to out'
        'If inverse==True, then f[i] is to self as i to out'
        n = self.n
        assert len(f) == n and sorted(set(f)) == list(
            range(n)), f'Invalid permutation {f}'
        if inverse:
            inv = [0] * n
            for i in range(n):
                inv[f[i]] = i
            f = inv
        leq = self.leq
        out = np.zeros_like(leq)
        for i in range(n):
            for j in range(n):
                out[f[i], f[j]] = leq[i, j]
        out.flags.writeable = False
        out_labels: Optional[Sequence[str]]
        if reset_labels:
            out_labels = None
        else:
            out_labels = ['' for i in range(n)]
            for i in range(n):
                out_labels[f[i]] = self.labels[i]
            out_labels = tuple(out_labels)
        return self.__class__(out, labels=out_labels)

    def relabel(self, labels=None):
        'copy of self with different labels'
        return self.__class__(self.leq, labels=labels)

    @cached_property
    def canonical(self):
        'equivalent poset with enumerated labels and stable order'
        n = self.n
        group_by = {h: [] for h in range(n)}
        for i in range(n):
            group_by[self.heights[i]].append(i)
        topo = []
        rank = [-1] * n
        G = self.parents
        R = self.children
        nleq = self.leq.sum(axis=0)
        ngeq = self.leq.sum(axis=1)
        order = list(zip(nleq, ngeq, self.hash_elems, self.labels, range(n)))

        def key(i):
            t = tuple(sorted((rank[i] for i in R[i])))
            return (t, len(G[i]), order[i])

        for h in range(n):
            for i in sorted(group_by[h], key=key):
                rank[i] = len(topo)
                topo.append(i)
        leq = self.reindex(rank).leq
        return self.__class__(leq, labels=None)

    '''
    @section
        Methods for atomic changes (grow-by-one inductively)
    # '''

    # def _iter_velid_edges(self, redundant=False):
    #     '''Edges that if added, the result is still a lattice'''
    #     assert self.is_lattice
    #     n = self.n
    #     leq = self.leq
    #     lt = leq.copy()
    #     lt[np.diag_indices_from(lt)] = 0
    #     gt = lt.T
    #     for i, j in product_list(range(n), repeat=2):
    #         if leq[j, i]:
    #             valid = False
    #         elif lt[i, j]:
    #             valid = redundant
    #         elif nocmp[i, j]:
    #             Xij = np.flatnonzero(lt[j] & ~lt[j])
    #             Yij = np.flatnonzero(gt[i] & ~gt[j])
    #             valid = not any(leq[x, y] for x, y in product(Xij, Yij))
    #         if valid:
    #             yield i, j
    #     return

    def _add_edge(self, i, j, assume_poset=False):
        "Grow self by adding one edge 'i leq j'"
        leq = self.leq
        new_leq = leq + np.matmul(leq[:, i:i + 1], leq[j:j + 1, :])
        new_leq.flags.writeable = False
        obj = self.__class__(new_leq, _validate=False)
        if not assume_poset:
            _ = obj.toposort
        return obj

    def _add_node(self, i, j, assume_poset=False):
        "Grow self by adding one node just between i and j"
        n = self.n
        leq = self.leq
        out = np.zeros((n + 1, n + 1), bool)
        out[:-1, :-1] = leq
        out[n, n] = True
        out[:-1, :-1] += np.matmul(leq[:, i:i + 1], leq[j:j + 1, :])
        out[n, :-1] = leq[j, :]
        out[:-1, n] = leq[:, i]
        out.flags.writeable = False
        obj = self.__class__(out)
        if not assume_poset:
            _ = obj.toposort
        return obj

    @cached_property
    def forbidden_pairs(self):
        "Pairs (i,j) that break lub uniqueness or partial order structure"
        n = self.n
        leq = self.leq
        joi = self.lub
        nocmp = ~(leq + leq.T)

        def f(a, b):
            if leq[b, a]:
                return True
            if leq[a, b]:
                return False
            X = [x for x in range(n) if leq[x, a]]
            Y = [y for y in range(n) if ~leq[b, y] and nocmp[y, a]]
            return any(nocmp[joi[x, y], joi[b, y]] for y in Y for x in X)

        fb = np.array([[f(i, j) for j in range(n)] for i in range(n)],
                      dtype=bool)
        return fb

    def iter_add_edge(self):
        "Grow self by adding one edge"
        n = self.n
        leq = self.leq
        fb = self.forbidden_pairs
        vis = set()
        h = self.hash_elems
        for i, j in product_list(range(n), repeat=2):
            if not fb[i, j] and not leq[i, j] and (h[i], h[j]) not in vis:
                yield self._add_edge(i, j, assume_poset=True)
        return

    def iter_add_node(self):
        "Grow self by adding one node"
        n = self.n
        leq = self.leq
        fb = self.forbidden_pairs
        vis = set()  # Don't repeat isomorphical connections
        h = self.hash_elems
        for i, j in product_list(range(n), repeat=2):
            if not fb[i, j] and not (h[i], h[j]) in vis:
                yield self._add_node(i, j, assume_poset=True)
        return

    @classmethod
    def iter_all_latices(cls, max_size):
        q = deque([cls.from_children(x) for x in [[], [[]], [[], [0]]]])
        vis = set()
        while q:
            U = q.popleft()
            yield U.canonical
            it = U.iter_add_node() if U.n < max_size else iter([])
            for V in chain(U.iter_add_edge(), it):
                if V not in vis:
                    vis.add(V)
                    q.append(V)

    @classmethod
    def all_latices(cls, max_size):
        return list(cls.iter_all_latices(max_size))

    '''
    @section
        Methods for all endomorphisms
    '''

    def iter_f_all(self):
        'all endomorphisms'
        return product_list(range(self.n), repeat=self.n)

    @cached_property
    def num_f_all(self):
        return self.n**self.n

    def iter_f_all_bottom(self):
        'all endomorphisms f with f[bottom]=bottom'
        n = self.n
        if n > 0:
            options = [range(n) if i != self.bottom else [i] for i in range(n)]
            for f in product_list(*options):
                yield f
        return

    @cached_property
    def num_f_all_bottom(self):
        return self.n**(self.n - 1)

    '''
    @section
        Methods for all monotonic endomorphisms
    '''

    def f_is_monotone(self, f, domain=None):
        'check if f is monotone over domain'
        n = self.n
        domain = range(n) if domain is None else domain
        leq = self.leq
        for i in domain:
            for j in domain:
                if leq[i, j] and not leq[f[i], f[j]]:
                    return False
        return True

    def iter_f_monotone_bruteforce(self):
        'all monotone functions'
        for f in self.iter_f_all():
            if self.f_is_monotone(f):
                yield f
        return

    def iter_f_monotone_bottom_bruteforce(self):
        'all monotone functions with f[bottom]=bottom'
        for f in self.iter_f_all_bottom():
            if self.f_is_monotone(f):
                yield f
        return

    def iter_f_monotone(self):
        'all monotone functions'
        f = [None] * self.n
        yield from self.iter_f_monotone_restricted(_f=f)

    def iter_f_lub_bruteforce(self):
        'all space functions. Throws if no bottom'
        for f in self.iter_f_monotone_bottom():
            if self.f_is_lub_pairs(f):
                yield f
        return

    def iter_f_monotone_restricted(self, domain=None, _f=None):
        'generate all monotone functions f : domain -> self, padding non-domain with None'
        n = self.n
        leq = self.leq
        geq_list = [[j for j in range(n) if leq[i, j]] for i in range(n)]
        f = [None for i in range(n)] if _f is None else _f
        topo, children = self._toposort_children(domain)
        yield from self._iter_f_monotone_restricted(f, topo, children, geq_list)

    def _iter_f_monotone_restricted(self, f, topo, children, geq_list):
        n = self.n
        m = len(topo)
        lub = self.lub
        _lub_f = (lambda acum, b: lub[acum, f[b]])
        lub_f = lambda elems: reduce(_lub_f, elems, self.bottom)

        def backtrack(i):
            'f[topo[j]] is fixed for all j<i. Backtrack f[topo[k]] for all k>=i, k<m'
            if i == m:
                yield f
            else:
                for k in geq_list[lub_f(children[i])]:
                    f[topo[i]] = k
                    yield from backtrack(i + 1)

        yield from backtrack(0)

    def _toposort_children(self, domain):
        'Compute a toposort for domain and the children lists filtered for domain'
        'j in out.children[i] iff j in out.topo and j is children of out.topo[i]'
        n = self.n
        D = range(n) if domain is None else domain
        topo = [i for i in self.toposort if i in D]
        sub = self.subgraph(topo)
        children = [[topo[j] for j in l] for l in sub.children]
        return topo, children

    def iter_f_monotone_bottom(self):
        'all monotone functions with f[bottom]=bottom'
        if not self.n:
            return
        f: List[Optional[int]] = [None] * self.n
        f[self.bottom] = self.bottom
        domain = [i for i in range(self.n) if i != self.bottom]
        yield from self.iter_f_monotone_restricted(domain=domain, _f=f)

    '''
    @section
        Methods for monotonic endomorphisms over irreducibles
    '''

    @cached_property
    def irreducible_components(self):
        'components of join irreducibles in toposort order and children lists for each component'
        n = self.n
        if n <= 1:  # no join irreducibles at all
            return (0, [], [])
        irr = self.irreducibles
        sub = self.subgraph(irr)
        subcomps = sub.independent_components
        m = len(subcomps)
        irrcomps = [[irr[j] for j in subcomps[i]] for i in range(m)]
        m_topo, m_children = zip(
            *(self._toposort_children(irrcomps[i]) for i in range(m)))
        return m, m_topo, m_children

    def _interpolate_funcs(self, funcs, domain) -> Iterable[List[int]]:
        'extend each f in funcs outside domain using f[j]=lub(f[i] if i<=j and i in domain)'
        n = self.n
        lub = self.lub
        leq = self.leq
        bot = self.bottom
        no_domain = [i for i in range(n) if i not in domain]
        dom_leq = [[i for i in domain if leq[i, j]] for j in range(n)]
        lub_f = (lambda a, b: lub[a, b])
        for f in funcs:
            for j in no_domain:
                f[j] = reduce(lub_f, (f[x] for x in dom_leq[j]), bot)
            yield f

    def iter_f_irreducibles_monotone_bottom(self) -> Iterable[List[int]]:
        'all functions given by f[non_irr]=lub(f[irreducibles] below non_irr)'
        if self.n == 0:
            return
        n = self.n
        leq = self.leq
        geq_list = [[j for j in range(n) if leq[i, j]] for i in range(n)]
        m, m_topo, m_children = self.irreducible_components
        f = [None for i in range(n)]

        def backtrack(i):
            if i == m:
                yield f
            else:
                for _ in self._iter_f_monotone_restricted(
                        f, m_topo[i], m_children[i], geq_list):
                    yield from backtrack(i + 1)

        funcs = backtrack(0)
        yield from self._interpolate_funcs(funcs, self.irreducibles)

    def iter_f_irreducibles_monotone(self):
        'all functions given by f[non_irr]=lub(f[irreducibles] below non_irr) and'
        'f[bottom] = any below or equal to glb(f[irreducibles])'
        n = self.n
        if n == 0:
            return
        glb = self.glb
        leq = self.leq
        below = [[i for i in range(n) if leq[i, j]] for j in range(n)]
        bottom = self.bottom
        irreducibles = self.irreducibles
        for f in self.iter_f_irreducibles_monotone_bottom():
            _glb_f = (lambda acum, b: glb[acum, f[b]])
            glb_f = lambda elems: reduce(_glb_f, elems, self.top)
            for i in below[glb_f(irreducibles)]:
                f[bottom] = i
                yield f

    '''
    @section
        Methods for endomorphisms that preserve lub
    '''

    def f_is_lub(self, f, domain=None):
        'check if f preserves lubs for sets:\n'
        'check f_is_lub_pairs and and f[bottom]=bottom.\n'
        'Throws if no bottom'
        n = self.n
        if n == 0 or (domain is not None and len(domain) <= 1):
            return True
        bot = self.bottom
        if f[bot] != bot or (domain is not None and bot not in domain):
            return False
        return self.f_is_lub_pairs(f, domain)

    def f_is_lub_pairs(self, f, domain=None):
        'check if f preserves lubs for pairs: f[lub[i,j]]=lub[f[i],f[j]]'
        n = self.n
        domain = range(n) if domain is None else domain
        lub = self.lub
        for i in domain:
            for j in domain:
                if f[lub[i, j]] != lub[f[i], f[j]]:
                    return False
        return True

    def iter_f_lub_pairs_bruteforce(self):
        'all functions that statisfy f_is_lub_pairs'
        for f in self.iter_f_monotone():
            if self.f_is_lub_pairs(f):
                yield f
        return

    def iter_f_lub_pairs(self):
        'all functions that statisfy f_is_lub'
        it = self.iter_f_irreducibles_monotone()
        if self.is_distributive:
            yield from it
        else:
            for f in it:
                if self.f_is_lub_pairs(f):
                    yield f

    def iter_f_lub(self):
        'all functions that preserve lubs for sets'
        it = self.iter_f_irreducibles_monotone_bottom()
        if self.is_distributive:
            yield from it
        else:
            for f in it:
                if self.f_is_lub_pairs(f):
                    yield f

    @cached_property
    def num_f_lub_pairs(self):
        return self.count_f_lub_pairs_bruteforce()

    def count_f_lub_pairs_bruteforce(self):
        return sum(1 for f in self.iter_f_lub_pairs())

    @cached_property
    def num_f_lub(self):
        return self.count_f_lub()

    def count_f_lub(self):
        if self.is_distributive:
            num = self.count_f_lub_distributive()
        else:
            num = self.count_f_lub_bruteforce()
        return num

    def count_f_lub_bruteforce(self):
        return sum(1 for f in self.iter_f_lub())

    '''
    @section
        Methods and optimizations for distributive lattices
    '''

    @cached_property
    def is_distributive(self):
        return self.explain_non_distributive is None

    @cached_property
    def explain_non_distributive(self):
        'Find i, j, k that violate distributivity. None otherwise'
        n = self.n
        lub = self.lub
        glb = self.glb
        for i in range(n):
            diff = glb[i, lub] != lub[np.ix_(glb[i, :], glb[i, :])]
            if diff.any():
                j, k = next(zip(*np.where(diff)))  # type:ignore
                return (
                    f'Non distributive lattice:\n'
                    f'{i} glb ({j} lub {k}) = {i} glb {lub[j,k]} = '
                    f'{glb[i,lub[j,k]]} != {lub[glb[i,j],glb[i,k]]} = '
                    f'{glb[i,j]} lub {glb[i,k]} = ({i} glb {j}) lub ({i} glb {k})'
                )
        return None

    def assert_distributive(self):
        if not self.is_distributive:
            hook = lambda: print(self.explain_non_distributive)
            raise PosetExceptions.NotDistributiveException(hook)

    def iter_f_lub_distributive(self):
        'generate and interpolate all monotone functions over irreducibles'
        self.assert_distributive()
        yield from self.iter_f_irreducibles_monotone_bottom()

    def count_f_lub_distributive(self):
        self.assert_distributive()
        if self.n == 0:
            return 0
        n = self.n
        leq = self.leq
        geq_list = [[j for j in range(n) if leq[i, j]] for i in range(n)]
        m, m_topo, m_children = self.irreducible_components
        f = [None for i in range(n)]

        def num(i):
            'num of monotone functions restricted to domain k_topo[i]'
            it = self._iter_f_monotone_restricted(f, m_topo[i], m_children[i],
                                                  geq_list)
            return sum(1 for _ in it)

        k_independent = [num(k) for k in range(m)]
        return reduce(lambda a, b: a * b, k_independent, 1)

    '''
    @section
        Methods and optimizations for modular lattices
    '''

    @cached_property
    def is_modular(self):
        return self.explain_non_modular is None

    @cached_property
    def explain_non_modular(self):
        'Find i, j, k that violate modularity. None otherwise'
        n = self.n
        lub = self.lub
        glb = self.glb
        problem = lambda i, j, k: (
            f'Non modular lattice:\n'
            f'{i} leq {k} and '
            f'{i} glb ({j} lub {k}) = {i} glb {lub[j,k]} = '
            f'{glb[i,lub[j,k]]} != {lub[glb[i,j],glb[i,k]]} = '
            f'{glb[i,j]} lub {glb[i,k]} = ({i} glb {j}) lub ({i} glb {k})')
        for i in range(n):
            diff = glb[i, lub] != lub[np.ix_(glb[i, :], glb[i, :])]
            if diff.any():
                issues: List[Tuple[int, int]]
                issues = list(zip(*np.where(diff)))  # type:ignore
                for j, k in issues:
                    if lub[i, k] == k:
                        return problem(i, j, k)
        return None

    def assert_modular(self):
        if not self.is_modular:
            hook = lambda: print(self.explain_non_modular)
            raise PosetExceptions.NotModularException(hook)

    '''
    @section
        Methods for high level (meta) relatives of self 
    '''

    @cached_property
    def meta_J(self):
        'subposet of join irreducibles'
        assert self.is_distributive
        return self.subgraph(self.irreducibles)

    @cached_property
    def meta_O(self):
        'distributive lattice of the closure of downsets of self'
        n = self.n
        leq = self.leq
        labels = self.labels
        P_down = [frozenset(i for i in range(n) if leq[i, j]) for j in range(n)]
        P_layer = [set() for i in range(n + 1)]
        for s in P_down:
            P_layer[len(s)].add(s)

        def iter_diff(a):
            n = len(a)
            yield from ((a[i], a[j]) for i in range(n) for j in range(i + 1, n))

        E = []
        layer: Sequence[Set] = []
        layer.append(set([frozenset()]))
        for k in range(n):
            layer.append(P_layer[k + 1])
            for u in P_layer[k + 1]:
                for below in layer[k]:
                    if below <= u:
                        E.append((below, u))
            for u, v in iter_diff(list(layer[k])):
                if u & v in layer[k - 1]:
                    above = u | v
                    layer[k + 1].add(above)
                    E.append((v, above))
                    E.append((u, above))
        nodes = list(set(u for u, v in E) | set(v for u, v in E))
        encode = {s: i for i, s in enumerate(nodes)}
        children = [[] for i in range(len(nodes))]
        for s, r in E:
            children[encode[r]].append(encode[s])
        label_of = lambda s: '{' + ','.join(self._label(*sorted(s))) + '}'
        labels = tuple(map(label_of, nodes))
        return self.__class__.from_children(children, labels=labels)

    def _label(self, *nodes):
        return tuple(self.labels[x] for x in nodes)

    def _meta_mat(self, F, leq_F):
        n = self.n
        leq = self.leq
        m = len(F)
        mat = np.zeros((m, m), dtype=bool)
        for i in range(m):
            for j in range(m):
                mat[i, j] = leq_F(F[i], F[j])
        mat.flags.writeable = False
        return mat

    @cached_property
    def meta_E(self):
        'lattice of join endomorphisms of self'
        elems = list(map(tuple, self.iter_f_irreducibles_monotone_bottom()))
        labels = tuple(','.join(self._label(*f)) for f in elems)
        return self.__class__.from_lambda(elems, self._leq_E, labels=labels)

    def _leq_E(self, f, g):
        'natural order of the space of endomorphisms'
        n = self.n
        leq = self.leq
        return all(leq[f[i], g[i]] for i in range(n))

    @cached_property
    def meta_JE(self):
        'poset of functions that are join irreducibles in meta_E'
        'this is equivalent to meta_E.meta_J'
        n = self.n
        leq = self.leq
        bot = self.bottom
        J = self.irreducibles
        f = lambda i, fi: tuple(bot if not leq[i, x] else fi for x in range(n))
        elems = [f(i, fi) for i in J for fi in J]
        labels = tuple(','.join(self._label(*f)) for f in elems)
        return self.__class__.from_lambda(elems, self._leq_E, labels=labels)

    @cached_property
    def meta_JJ(self):
        'poset of self upside down times self, i.e. (~self)*self'
        'with labels showing homomorphism with meta_O.meta_JE'
        n = self.n
        leq = self.leq
        elems = [(i, fi) for i in range(n) for fi in range(n)]
        label_of = lambda i, fi: f'f({i})={fi}'
        labels = tuple(label_of(*self._label(i, fi)) for i, fi in elems)

        def f_leq(tup_i, tup_j):
            i, fi = tup_i
            j, fj = tup_j
            return leq[j, i] and leq[fi, fj]

        return self.__class__.from_lambda(elems, f_leq, labels=labels)

    '''
    @section
        Constructors and operations between lattices
    '''

    @classmethod
    def total(cls, n):
        'total order of n elements'
        G = [[i - 1] if i > 0 else [] for i in range(n)]
        return cls.from_children(G)

    def __invert__(self):
        'flip the poset upside down'
        cls = self.__class__
        return cls.from_children(self.parents, labels=self.labels)

    def __add__(self, other):
        if isinstance(other, int):
            out = self.add_number(other)
        else:
            out = self.add_poset(other)
        return out

    def __mul__(self, other):
        if isinstance(other, int):
            out = self.mul_number(other)
        else:
            out = self.mul_poset(other)
        return out

    def __or__(self, other):
        if isinstance(other, int):
            out = self.or_number(other)
        else:
            out = self.or_poset(other)
        return out

    def __and__(self, other):
        if isinstance(other, int):
            out = self.and_number(other)
        else:
            out = self.and_poset(other)
        return out

    def add_poset(self, other):
        'stack other above self and connect all self.tops with all other.bottoms'
        cls = self.__class__
        n = self.n
        C = [
            *([j for j in Ci] for Ci in self.children),
            *([j + n for j in Ci] for Ci in other.children),
        ]
        for i in self.tops:
            for j in other.bottoms:
                C[j + n].append(i)
        return cls.from_children(C)

    def mul_poset(self, other):
        'poset standard multiplication'
        cls = self.__class__
        n = self.n
        m = other.n
        labels = [None] * (n * m)
        G = [[] for i in range(n * m)]
        for i in range(n):
            for j in range(m):
                for k in self.children[i]:
                    G[i + j * n].append(k + j * n)
                for k in other.children[j]:
                    G[i + j * n].append(i + k * n)
                labels[i + j * n] = f'({self.labels[i]},{other.labels[j]})'
        return cls.from_children(G, labels=labels)

    def or_poset(self, other):
        'put other at the right of self without connections'
        cls = self.__class__
        n = self.n
        C = [
            *([j for j in Ci] for Ci in self.children),
            *([j + n for j in Ci] for Ci in other.children),
        ]
        return cls.from_children(C)

    def and_poset(self, other):
        'stack other above self and put self.tops * other.bottoms inbetween'
        cls = self.__class__
        n = self.n
        nodes = [
            *((-1, i) for i in self.non_tops),
            *((i, j) for i in self.tops for j in other.bottoms),
            *((n, j) for j in other.non_bottoms),
        ]
        C = {v: [] for v in nodes}
        for i in self.non_tops:
            for j in self.children[i]:
                C[(-1, i)].append((-1, j))
        for i in other.non_bottoms:
            for j in other.parents[i]:
                C[(n, j)].append((n, i))
        for i in self.tops:
            for j in self.children[i]:
                for k in other.bottoms:
                    C[(i, k)].append((-1, j))
        for i in other.bottoms:
            for j in other.parents[i]:
                for k in self.tops:
                    C[(n, j)].append((k, i))
        f = {node: i for i, node in enumerate(sorted(nodes))}
        children = [[] for i in range(len(f))]
        for i, Ci in C.items():
            for j in Ci:
                children[f[i]].append(f[j])
        return cls.from_children(children)

    def add_number(self, n):
        'add self with itself n times'
        assert isinstance(n, int) and n >= 0, f'{n}'
        cls = self.__class__
        if n == 0:
            out = cls.total(0)
        else:
            out = self._operation_number(lambda a, b: a + b, n)
        return out

    def mul_number(self, n):
        'multiply self with itself n times'
        assert isinstance(n, int) and n >= 0, f'{n}'
        cls = self.__class__
        if n == 0:
            out = cls.total(1)
        else:
            out = self._operation_number(lambda a, b: a * b, n)
        return out

    def or_number(self, n):
        'OR operation of self with itself n times'
        assert isinstance(n, int) and n >= 0, f'{n}'
        cls = self.__class__
        if n == 0:
            out = cls.total(0)
        else:
            out = self._operation_number(lambda a, b: a | b, n)
        return out

    def and_number(self, n):
        'AND operation of self with itself n times'
        assert isinstance(n, int) and n >= 0, f'{n}'
        cls = self.__class__
        if n == 0:
            out = cls.total(1)
        else:
            out = self._operation_number(lambda a, b: a & b, n)
        return out

    def _operation_number(self, operation, n):
        'operate self with itself n>=1 times. operation must be associative'
        if n == 1:
            out = self
        else:
            out = self._operation_number(operation, n // 2)
            out = operation(out, out)
            if n % 2 == 1:
                out = operation(out, self)
        return out

    '''
    @section
        Testing methods
    '''

    def _test_iters_diff(self, it1, it2):
        '''Compute set1 = set(it1)-set(it2) and set2 = set(it2)-set(it1)
        Assumes that the iterators do not repeat elements'''
        set1 = set()
        set2 = set()
        for x, y in zip(it1, it2):
            if x != y:
                if x in set2:
                    set2.discard(x)
                else:
                    set1.add(x)
                if y in set1:
                    set1.discard(y)
                else:
                    set2.add(y)
        for x in it1:
            set1.add(x)
        for y in it2:
            set2.add(y)
        return set1, set2

    def _test_iters(self, it1, it2):
        'Check if two iterators yield the same values'

        def timed(it, key):
            cnt = total = 0
            t = time.time()
            for i in it:
                total += time.time() - t
                yield i
                t = time.time()
                cnt += 1
            times[key] = total
            count[key] = cnt

        times = {}
        count = {}
        it1 = timed(it1, 0)
        it2 = timed(it2, 1)
        set1, set2 = self._test_iters_diff(it1, it2)
        same = not set1 and not set2
        reason = not same and (f'Iterators are different:\n'
                               f'Found by 1 not by 2: {set1}\n'
                               f'Found by 2 not by 1: {set2}')
        self._test_summary(times, count, same, reason)

    def _test_counts(self, f1, f2):
        times = {}
        count = {}
        t = time.time()
        count[0] = f1()
        times[0] = time.time() - t
        t = time.time()
        count[1] = f2()
        times[1] = time.time() - t
        same = count[0] == count[1]
        reason = not same and (f'Methods are different:\n'
                               f'Output of 1: {count[0]}\n'
                               f'Output of 2: {count[1]}')
        self._test_summary(times, count, same, reason)

    def _test_summary(self, times, count, same, reason):
        print(f'repr: {self}\n'
              f'hash: {hash(self)}\n'
              f'n: {self.n}\n'
              f'is_distributive: {self.is_distributive}\n'
              f'Time used by method 1: {round(times[0], 2)}s\n'
              f'Time used by method 2: {round(times[1], 2)}s\n'
              f'Elements found by method 1: {count[0]}\n'
              f'Elements found by method 2: {count[1]}\n'
              f'Same output: {same}\n')
        if not same:
            self.describe()
            raise Exception(reason)

    def _test_assert_distributive(self):
        try:
            self.assert_distributive()
        except PosetExceptions.NotDistributiveException:
            print(
                'The test can not be executed because the lattice is not distributive'
            )
            raise

    def test_iter_f_monotone(self, outfile=None):
        it1 = map(tuple, self.iter_f_monotone())
        it2 = map(tuple, self.iter_f_monotone_bruteforce())
        with Outfile(outfile):
            self._test_iters(it1, it2)

    def test_iter_f_monotone_bottom(self, outfile=None):
        it1 = map(tuple, self.iter_f_monotone_bottom())
        it2 = map(tuple, self.iter_f_monotone_bottom_bruteforce())
        with Outfile(outfile):
            self._test_iters(it1, it2)

    def test_iter_f_lub(self, outfile=None):
        it1 = map(tuple, self.iter_f_lub())
        it2 = map(tuple, self.iter_f_lub_bruteforce())
        with Outfile(outfile):
            self._test_iters(it1, it2)

    def test_iter_f_lub_pairs(self, outfile=None):
        it1 = map(tuple, self.iter_f_lub_pairs())
        it2 = map(tuple, self.iter_f_lub_pairs_bruteforce())
        with Outfile(outfile):
            self._test_iters(it1, it2)

    def test_iter_f_lub_distributive(self, outfile=None):
        self._test_assert_distributive()
        it1 = map(tuple, self.iter_f_lub())
        it2 = map(tuple, self.iter_f_lub_distributive())
        with Outfile(outfile):
            self._test_iters(it1, it2)

    def test_count_f_lub_distributive(self, outfile=None):
        self._test_assert_distributive()
        f1 = lambda: self.count_f_lub_distributive()
        f2 = lambda: self.count_f_lub_bruteforce()
        with Outfile(outfile):
            self._test_counts(f1, f2)

    '''
    @section
        Methods for serialization
    '''

    def to_literal(self, keys=None):
        '''Json serializable representation of self that also stores
        some expensive cached data'''
        out = self.__dict__.copy()
        for key, value in out.items():
            if keys is None or key in keys:
                if isinstance(value, np.ndarray):
                    out[key] = {
                        'dtype': get_dtype_string(value.dtype),
                        'array': value.tolist()
                    }
        return out

    @classmethod
    def from_literal(cls, lit):

        def read_numpy_array(dict_):
            arr = np.array(dict_['array'], dtype=dict_['dtype'])
            if arr.size == 0:
                arr = arr.reshape((0, 0))
            arr.flags.writeable = False
            return arr

        V = cls(read_numpy_array(lit.pop('leq')))
        for key, value in lit.items():
            if isinstance(value,
                          dict) and 'dtype' in value and 'array' in value:
                value = read_numpy_array(value)
            V.__dict__[key] = value
        return V

    '''
    @section
        Methods for interactive definition of other methods
    '''

    @classmethod
    def set_method(cls, method):
        assert hasattr(method, '__call__'), f'Not callable method: {method}'
        setattr(cls, method.__name__, method)

    @classmethod
    def set_classmethod(cls, method):
        assert hasattr(method, '__call__'), f'Not callable method: {method}'
        setattr(cls, method.__name__, classmethod(method))

    @classmethod
    def set_staticmethod(cls, method):
        assert hasattr(method, '__call__'), f'Not callable method: {method}'
        setattr(cls, method.__name__, staticmethod(method))

    @classmethod
    def set_property(cls, method):
        assert hasattr(method, '__call__'), f'Not callable method: {method}'
        setattr(cls, method.__name__, property(method))

    '''
    @section
        Random generation of posets 
    '''

    @classmethod
    def random_poset(cls, n: int, p: float, seed=None):
        '''
        Generates a random poset.
        All posets (modulo labels) have positive probability of being generated.
        If p is close to 0, the poset is very sparse.
        If p is close to 1, the poset is very dense.
        '''
        R = np.random.RandomState(seed=seed)
        rel = np.zeros((n, n), dtype=bool)
        for i in range(n):
            for j in range(i + 1, n):
                if R.random() < p:
                    rel[i, j] = 1
        for i in range(n):
            rel[i, i] = 1
        rel.flags.writeable = False
        leq = Relation(rel).transitive_closure().rel
        poset = cls(leq, _validate=False)
        return poset

    @classmethod
    def random_lattice_czech(cls, n: int, seed=None):
        '''
        Description: http://ka.karlin.mff.cuni.cz/jezek/093/random.pdf
        '''
        lub = random_lattice_czech(n, seed)
        rel = (lub <= np.arange(n)[None, :])
        rel.flags.writeable = False
        poset = cls(rel, _validate=True)
        try:
            if poset.n > 0:
                poset.bottom
        except NotUniqueBottomException:
            # Fix bottoms:
            bottoms = poset.bottoms
            bot = bottoms[0]
            rel.flags.writeable = True
            for i in bottoms:
                rel[bot, i] = True
            rel.flags.writeable = False
            rel = Relation(rel).transitive_closure().rel
            poset = cls(rel, _validate=True)
            poset.assert_lattice()
        return poset

    # @classmethod
    # def random_modular(cls):
    #     return

    # @classmethod
    # def random_distributive(cls):
    #     return
    '''
    @section
        Methods related with entropy
    '''

    def count_antichains_bruteforce(self):
        return self.brute_downset_closure.n

    @cached_property
    def num_antichains(self):
        return self.count_antichains_bruteforce()

    @cached_property
    def brute_downset_closure(self):
        n = self.n
        leq = self.leq
        sets = set([frozenset()])
        last = set(
            frozenset(j for j in range(n) if leq[j, i]) for i in range(n))
        while last:
            curr = set(c for a in last
                       for b in last for c in (a | b, a & b) if c not in sets)
            sets |= last
            last = curr
        f = {s: i for i, s in enumerate(sorted(sets, key=lambda s: len(s)))}
        E = [(f[b], f[a]) for a in sets for b in sets if a < b]
        return self.__class__.from_down_edges(len(sets), E)

    '''
    @section
        Help and examples
    '''

    def help_verbose(self):
        return '''
        Except for n, leq and labels, all other attributes are
        lazy loaded and usually cached.
        
        Conventions:
            - child[i,j]==True iff j covers i (with no elements inbetween)
            - children[j] = [i for i in range(n) if leq[i,j]]
            - parents[i] = [j for j in range(n) if leq[i,j]]

            For lattices:
                - lub[i,j] is the least upper bound for i and j.
                - glb[i,j] is the greatest lower bound for i and j
        
        Requires external packages:
            - numpy
            - cached_property
            - pyhash
            - pydotplus (which needs graphviz 'dot' program)

        Why pyhash?
            Because it is stable (like hashlib) and fast (like hash).
            hashlib is not adequate because it adds an unnecessary computation footrint.
            hash(tuple(...)) is not adequate because it yields different results across
            several runs unless PYTHONHASHSEED is set prior to execution.
        
        Examples:

        V = Poset.from_parents([[1,2],[],[],[1]])
        V.show()
        V = (V|Poset.total(1)).meta_O
        V.show()
        print(V.is_distributive)
        print(V.num_f_lub_pairs)
        for f in V.iter_f_lub_pairs_bruteforce():
            V.show(f)
            print(f)
        V.meta_O.show()
        '''

    '''
    @section
        Unclassified methods that will probably dissapear in the future
    '''

    def decompose_series(self):
        n = self.n
        leq = self.leq
        cmp = leq | leq.T
        nodes = sorted(range(n), key=lambda i: leq[:, i].sum())
        cuts = [i for i in nodes if cmp[i, :].sum() == n]
        subs = [nodes[i:j] for i, j in zip(cuts, cuts[1:])]
        return [self.subgraph(sub) for sub in subs]

    @classmethod
    def examples(cls):
        examples = {}
        grid = [[], [0], [0], [1], [1, 2], [2], [3, 4], [4, 5], [6, 7]]
        grid.extend([[0], [0], [9, 2], [10, 1]])
        for i, j in [(3, 9), (5, 10), (6, 11), (7, 12)]:
            grid[i].append(j)
        examples['portrait-2002'] = cls.from_children(grid)
        examples['portrait-2002'].__dict__['num_f_lub'] = 13858
        grid = [[], [0], [0], [1], [1, 2], [2], [3, 4], [4, 5], [6, 7]]
        grid = [[j + 9 * (i >= 9) for j in grid[i % 9]] for i in range(18)]
        for i, j in [(9, 4), (10, 6), (11, 7), (13, 8)]:
            grid[i].append(j)
        examples['portrait-1990'] = cls.from_children(grid)
        examples['portrait-1990'].__dict__['num_f_lub'] = 1460356
        examples['T1'] = cls.from_children([[]])
        examples['T2'] = cls.from_children([[], [0]])
        #for k in range(1, 10):
        #    examples[f'2^{k+1}'] = examples[f'2^{k}'] * examples[f'2^{k}']
        #examples['tower-crane'] =
        #examples['tower-crane'] =
        return examples

    @cached_property
    def num_paths_matrix(self):
        B = C = self.child.astype(int)
        A = np.zeros_like(B)
        A[np.diag_indices_from(A)] = 1
        while C.sum():
            A = A + C
            C = np.matmul(C, B)
        return A

    @cached_property
    def num_ace(self):
        d = self.dist
        A = self.num_paths_matrix
        bot = A[self.bottom, :]
        top = A[:, self.top]
        bot_top = A[self.bottom, self.top]
        middle = ((d == 2) * (bot[:, None] * top[None, :])).sum()
        return 2 * bot_top + (middle if self.n > 2 else 0)

    @classmethod
    def all_lattices_adding(cls, n: int):
        E = [pair for i in range(1, n - 1) for pair in [(0, i), (i, n - 1)]]
        MN_poset = cls.from_up_edges(n, E)
        num = {MN_poset: 0}
        V = [MN_poset]
        G = {0: []}
        q = deque([MN_poset])
        while q:
            P = q.popleft()
            for Q in P.iter_add_edge():
                if Q not in num:
                    num[Q] = len(V)
                    V.append(Q)
                    G[num[Q]] = []
                    q.append(Q)
                G[num[P]].append(num[Q])
        E = [(i, j) for i in G for j in G[i]]
        poset_of_posets = cls.from_up_edges(len(V), E)
        return V, poset_of_posets


def floyd_warshall(adj: npBoolMatrix, infinity: int) -> npUInt64Matrix:
    'Compute all pairs shortest distances using Floyd-Warshall algorithm'
    dist: npUInt64Matrix
    dist = adj.astype(np.uint64)  # type:ignore
    dist[~adj] = infinity
    dist[np.diag_indices_from(dist)] = 0
    for k in range(len(dist)):
        np.minimum(dist, dist[:, k, None] + dist[None, k, :], out=dist)
    return dist


_get_dtype_string = re.compile(
    r'(<class \'numpy\.(.*)\'>)|(<class \'(.*?)\'>)|(.*)')


def get_dtype_string(dtype):
    'return the dtype string of a numpy dtype'
    m = _get_dtype_string.match(str(dtype))
    assert m
    g = m.groups()
    dtype_str: str = g[1] or g[3] or g[4]
    np_dtype = np.dtype(dtype_str)  # type:ignore
    assert dtype == np_dtype, (
        f'Non invertible dtype: {dtype} != np.dtype(\'{dtype_str}\')')
    return dtype_str


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


class Outfile:
    '''
    Redirect stdout to a file inside statements like:
    with Outfile(...):
        print(...)
    '''

    def __init__(self, outfile=None):
        self.outfile = outfile

    def __enter__(self):
        if self.outfile is not None:
            self.initial_stdout = sys.stdout
            sys.stdout = open(self.outfile, 'a')

    def __exit__(self, *args):
        if self.outfile is not None:
            sys.stdout.close()
            sys.stdout = self.initial_stdout


def graphviz(
    n: int,
    edges: Sequence[Tuple[int, int]],
    labels: Sequence[str],
    blue_edges: Sequence[Tuple[int, int]] = None,
    save: str = None,
):
    'Show graph using graphviz. blue edges are extra edges'
    from pydotplus import graph_from_edges
    from pydotplus.graphviz import Node, Edge

    color = '#555555' if blue_edges is None else '#aaaaaa'

    g = graph_from_edges([], directed=True)
    g.set_rankdir('BT')  # type:ignore
    for i in range(n):
        style = {}
        g.add_node(Node(i, label=f'"{labels[i]}"', **style))
    for i, j in edges:
        style = {'dir': 'none', 'color': color}
        g.add_edge(Edge(i, j, **style))
    if blue_edges is not None:
        for i, j in blue_edges:
            style = {'color': 'blue', 'constraint': 'false'}
            g.add_edge(Edge(i, j, **style))

    png = g.create_png()  # type:ignore

    if save is None:
        import builtins
        if hasattr(builtins, '__IPYTHON__'):
            from IPython.display import display
            from IPython.display import Image
            img = Image(png)
            display(img)
        else:
            from io import BytesIO
            from PIL import Image
            img = Image.open(BytesIO(png))
            img.show()
    else:
        with open(save, 'wb') as f:
            f.write(png)
    return


import sys

sys.setrecursionlimit(10**6)


class Tarjan(list):
    vis: List[int]
    low: List[int]
    stack: List[int]
    in_stack: List[int]
    sccs: List[List[int]]
    vis_cnt: int

    def tarjan(self):
        G = self
        n = len(G)
        G.vis, G.low = [-1] * n, [0] * n
        G.stack, G.in_stack = [], [0] * n
        G.vis_cnt = 0
        G.sccs = []
        for i in range(n):
            if G.vis[i] == -1:
                G.dfs(i)
        invV = [-1] * n
        for i, scc in enumerate(G.sccs):
            for j in scc:
                invV[j] = i
        sccE = set()
        for i in range(n):
            for j in G[i]:
                sccE.add((invV[i], invV[j]))
        sccE = list(sccE)
        return G.sccs, sccE

    def dfs(self, i):
        G = self
        G.vis[i] = G.low[i] = G.vis_cnt
        G.vis_cnt += 1
        G.stack.append(i)
        G.in_stack[i] = 1
        for j in G[i]:
            if G.vis[j] == -1:
                G.dfs(j)
                G.low[i] = min(G.low[i], G.low[j])
            elif G.in_stack[j]:
                G.low[i] = min(G.low[i], G.vis[j])
        if G.low[i] == G.vis[i]:
            scc = []
            s = G.stack
            while s[-1] != i:
                scc.append(s.pop())
            scc.append(s.pop())
            for x in scc:
                G.in_stack[x] = 0
            G.sccs.append(scc)
        return

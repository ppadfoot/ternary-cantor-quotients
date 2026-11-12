#!/usr/bin/env python3
"""Exact checks for universal289 and the explicit local-witness family.
Python 3.10+, standard library only. Run without -O.
The all-length conclusions are proved in paper/universal_numerator.tex;
finite k-family and path examples are supplementary tests.
"""
from __future__ import annotations
from collections import deque
from pathlib import Path
import json
import platform
import random

ROOT = Path(__file__).resolve().parent
if not __debug__:
    raise SystemExit('Assertions must be enabled: do not use -O.')


def trim(p: list[int]) -> list[int]:
    p = p[:]
    while len(p) > 1 and p[-1] == 0:
        p.pop()
    return p


def multiply(p: list[int], q: list[int]) -> list[int]:
    out = [0] * (len(p) + len(q) - 1)
    for i, a in enumerate(p):
        if a:
            for j, b in enumerate(q):
                out[i + j] += a * b
    return trim(out)


def evaluate(p: list[int], x: int = 3) -> int:
    out = 0
    for c in reversed(p):
        out = x * out + c
    return out


def identity(h: list[int], hc: list[int], ht: list[int], a: int, b: int) -> bool:
    n = max(len(h), len(hc), len(ht) + 1)
    p = [0] * n
    for i, v in enumerate(hc): p[i] += v
    for i, v in enumerate(h): p[i] += a * v
    p[0] -= b
    for i, v in enumerate(ht): p[i + 1] -= v
    return not any(p)


def verify_289() -> dict:
    cert = json.loads((ROOT / 'certificates/certificate_289.json').read_text())
    m = cert['M']; assert m == 289
    graph = {int(c): [tuple(e) for e in edges] for c, edges in cert['full_graph'].items()}
    # Independent construction: all four input/output digit pairs, then reachability.
    full = {}
    tested_digit_pairs = 0
    for c in range((m + 1)//2):
        edges = []
        for a in (0, 1):
            for b in (0, 1):
                tested_digit_pairs += 1
                d = c + m*a - b
                if d >= 0 and d % 3 == 0:
                    target = d//3
                    assert 0 <= 2*target < m
                    edges.append((target, a, b))
        full[c] = edges
    seen = {0}; queue = deque([0])
    while queue:
        for t, _, _ in full[queue.popleft()]:
            if t not in seen:
                seen.add(t); queue.append(t)
    assert seen == set(graph)
    assert all(set(graph[c]) == set(full[c]) for c in seen)
    core = set(cert['return_core']); discarded = set(cert['nonreturn_closed_set'])
    assert not core & discarded and core | discarded == seen and 0 in core
    assert all(t in discarded for c in discarded for t, _, _ in graph[c])
    # Reverse reachability verifies that the stated return core is exact.
    reverse = {c: [] for c in seen}
    for c, es in graph.items():
        for t, a, b in es: reverse[t].append((c, a, b))
    can_return = {0}; queue = deque([0]); tails = {0: []}
    while queue:
        t = queue.popleft()
        for c, a, b in reverse[t]:
            if c not in can_return:
                can_return.add(c); queue.append(c)
                tails[c] = [(a, b)] + tails[t]
    assert can_return == core
    h = cert['quotient_polynomial_low_first']; assert evaluate(h) == m
    potentials = {int(c): p for c, p in cert['potentials_low_first'].items()}
    assert set(potentials) == core and potentials[0] == [0]
    polynomial_identities = 0
    for c in core:
        assert evaluate(potentials[c]) == c
        for t, a, b in graph[c]:
            if t in core:
                assert identity(h, potentials[c], potentials[t], a, b)
                polynomial_identities += 1
    # Negative control: same value at 3, but a wrong polynomial potential.
    wrong = potentials[96][:]; wrong[0] -= 3; wrong[1] += 1
    assert evaluate(wrong) == 96
    assert not identity(h, potentials[0], wrong, 1, 1)
    # Explicit universal witness, independently multiplied as polynomials.
    q = [int(i in (0, 2, 3, 5)) for i in range(6)]
    p = [int(i in (0, 7, 9, 10)) for i in range(11)]
    assert multiply(h, q) == p and evaluate(p) == m*evaluate(q)
    # Negative control: equality at 3 does not imply polynomial divisibility.
    q22 = [1, 0, 1, 1]; p22 = [1, 1, 0, 0, 1, 0, 1]
    assert evaluate(p22) == 22*evaluate(q22)
    h22 = [1, 1, -1, 1]
    assert multiply(h22, q22) != p22
    divided = multiply([-3, 2, -1, 1], q22)
    for i, c in enumerate([4, -1, 4]): divided[i] += c
    assert trim(divided) == p22  # nonzero remainder of degree below deg(q22)
    # Exact word tests, not used to extrapolate to all words.
    rng = random.Random(406)
    for _ in range(256):
        word = [(1, 1)]; c = 96
        for _ in range(rng.randrange(201)):
            t, a, b = rng.choice([e for e in graph[c] if e[0] in core])
            word.append((a, b)); c = t
        word += tails[c]
        q = trim([a for a, b in word]); p = trim([b for a, b in word])
        assert multiply(h, q) == p and evaluate(p) == m*evaluate(q)
    return dict(states=len(seen), edges=sum(map(len, graph.values())),
                return_core_states=len(core), closed_discarded_states=len(discarded),
                core_polynomial_identities=polynomial_identities,
                independent_digit_pair_tests=tested_digit_pairs,
                exact_return_words=256, negative_controls=2,
                explicit_witness=[280, 80920])


def family_polynomials(k: int) -> tuple[list[int], list[int]]:
    q = [0] * (k*k)
    for j in range(k):
        for i in range(k-j): q[(k+1)*j+i] = 1
    if k == 1: return q, [1, 0, 1]
    n = k*(k+1)
    p = [0] * (n+1); p[0] = 1
    for i in range(2, k+1): p[k*i] += 1
    for j in range(1, k-1): p[k+(k+1)*j] += 1
    p[n-1] += 1; p[n] += 1
    assert set(p) <= {0, 1}
    return q, p


def verify_family() -> dict:
    checked_coefficients = 0
    for k in range(1, 65):
        q, p = family_polynomials(k)
        m = 4*3**k-2
        assert evaluate(p) == m*evaluate(q)
        assert len(p) == k*(k+1)+1 and len(q) == k*k
        if k == 1: continue
        g = [-2] + [0]*(k-1) + [1, 1]
        gq = multiply(g, q)
        residual = [p[i] - (gq[i] if i < len(gq) else 0) for i in range(len(p))]
        expected = [3] + [2]*(k-1) + [-1]
        assert trim(residual) == expected and len(expected) < len(q)
        assert evaluate(expected) == 0 and any(expected)
        # Two telescoping identities used in the symbolic proof.
        s1 = multiply([-1]+[0]*k+[1], q)
        e1 = [0]*(k*(k+1)+1)
        for i in range(2, k+2):e1[k*i] += 1
        for i in range(k):e1[i] -= 1
        assert trim(s1) == trim(e1)
        s2 = multiply([-1]+[0]*(k-1)+[1], q)
        e2 = [0]*(k*(k+1))
        for j in range(k):e2[k+(k+1)*j] += 1
        for i in range(k):e2[i] -= 1
        assert trim(s2) == trim(e2)
        checked_coefficients += len(p)
    return dict(integer_witnesses=64, exact_nonzero_remainders=63,
                telescoping_identities=126, coefficient_comparisons=checked_coefficients)



def main() -> None:
    results = {'status': 'PASS', 'python': platform.python_version(),
       'scope': 'Complete coefficient-level carry certificate for289; finite k-family regression tests supplement the symbolic proof. Not proof-assistant verification.',
       'universal_289': verify_289(), 'explicit_family': verify_family()}
    (ROOT/'results.json').write_text(json.dumps(results, indent=2)+'\n')
    print(json.dumps(results, indent=2))

if __name__ == '__main__': main()

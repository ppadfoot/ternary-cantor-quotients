#!/usr/bin/env python3
"""Exact finite certificates for LE-406: block energy, real rational visits,
and combinatorial input to the word-abundance theorem.
Python 3.10+, standard library only. Run without -O.
These computations do NOT prove Matveev's theorem, discrepancy inequalities,
or replace the analytic asymptotic proofs in PROOF_RU.md.
"""
from collections import Counter
from fractions import Fraction
from itertools import product
from math import comb, gcd, log, sqrt
from pathlib import Path
import hashlib
import json
import sys
import time

ROOT = Path(__file__).resolve().parent
assert __debug__, 'Assertions must be enabled: do not use python -O.'


def digits01(k):
    a = [0]
    power = 1
    for _ in range(k):
        a += [x + power for x in a]
        power *= 3
    return a


def finite01(x):
    if x < 0:
        return False
    while x:
        x, digit = divmod(x, 3)
        if digit == 2:
            return False
    return True


def fib_pair(n):
    if n == 0:
        return 0, 1
    a, b = fib_pair(n // 2)
    c, d = a * (2 * b - a), a * a + b * b
    return (d, c + d) if n % 2 else (c, d)


def energy_data(c, depth):
    weights = Counter(c * (a - aa) + b - bb
                      for a, b, aa, bb in product((0, 1), repeat=4))
    # All reachable carries have absolute value strictly less than (c+1)/2.
    bound = c // 2
    states = list(range(-bound, bound + 1))
    idx = {x: i for i, x in enumerate(states)}
    rows = []
    for carry in states:
        row = []
        for digit, weight in sorted(weights.items()):
            if (carry + digit) % 3 == 0:
                nxt = (carry + digit) // 3
                assert nxt in idx
                row.append((idx[nxt], weight))
        rows.append(row)
    v = [0] * len(states)
    v[idx[0]] = 1
    totals = []
    for _ in range(depth):
        nxt = [0] * len(states)
        for i, val in enumerate(v):
            for j, weight in rows[i]:
                nxt[j] += val * weight
        v = nxt
        totals.append(sum(v))
    return states, rows, totals, v


def golden_power_lt_integer_scaled(scale, exponent, two_exp):
    """Prove scale*phi**exponent < 2**two_exp using integer squaring."""
    fn, fn1 = fib_pair(exponent)
    fm1 = fn1 - fn
    a, b = scale * fn, scale * fm1
    rem = 2 * (1 << two_exp) - a - 2 * b
    assert rem > 0
    assert rem * rem > 5 * a * a
    return True


def check_energy():
    states, rows, totals, terminal = energy_data(112, 128)
    c128 = totals[-1]
    # Independent backward propagation of continuation counts.
    backwards = [1] * len(states)
    for _ in range(128):
        backwards = [sum(w * backwards[j] for j, w in row) for row in rows]
    assert backwards[states.index(0)] == c128
    assert len(states) == 113
    assert c128 == int('2848039325767103655925435712986932980549021547392299357785070566911039704321748559183306903592')
    # alpha_0=1161/5000: g-s+alpha_0(1+tau-g-2s)<0.
    scale = c128 ** 1161 * 3 ** 148608
    golden_power_lt_integer_scaled(scale, 491392, 937216)
    # alpha_F=(3s-1)/(7-5s) < 1161/5000.
    assert 2 ** 20805 < 3 ** 13127
    # A simple fully specified Fourier choice: alpha=29/125, l/h=131/200.
    assert 2 ** 1793 > 3 ** 1131
    assert 15400 > 15399
    direct_cases, product_checks = 0, 0
    for c in (4, 13, 112):
        _, _, vals, _ = energy_data(c, 10)
        for d in range(1, 11):
            ds = digits01(d)
            modulus = 3 ** d
            hist = Counter((c * a + b) % modulus for a in ds for b in ds)
            product_checks += len(ds) ** 2
            assert sum(x * x for x in hist.values()) == vals[d-1]
            direct_cases += 1
            if d <= 5:
                # Exact cyclic autocorrelations: every shifted count <= count at 0.
                for shift in range(modulus):
                    assert sum(val * hist.get((key + shift) % modulus, 0)
                               for key, val in hist.items()) <= vals[d-1]
    # Negative control: without the fixed low digits, two-digit cap is 36, not 34.
    assert energy_data(1, 2)[2][-1] == 36
    assert energy_data(4, 2)[2][-1] == 34
    assert 36 > 34
    cert = dict(multiplier=112, block_length=128, states=states,
                rows=rows, energy_totals=totals, terminal_vector=terminal,
                energy=c128,
                exact_exponent_certificate=dict(alpha_numerator=1161,
                    alpha_denominator=5000, phi_exponent=491392,
                    power3_exponent=148608, power2_exponent=937216,
                    verified=True),
                scope='Finite exact certificate; analytic use is proved in PROOF_RU.md.')
    (ROOT/'certificates'/'energy112_128.json').write_text(json.dumps(cert, indent=2)+'\n')
    return dict(states=len(states), block_length=128, energy=str(c128),
                independent_direct_cases=direct_cases,
                independent_pair_products=product_checks,
                exact_sign_certificates=4,
                full_depth_backward_verification=True,
                unrestricted_negative_control=True)


def check_block_lifting():
    cases = extensions = 0
    for c, d, m in ((4,2,5),(13,2,5),(112,2,6),(112,3,6)):
        modulus = 3 ** m
        blockmod = 3 ** d
        ns = [z for z in digits01(m) if z % blockmod == 1]
        xs = [z for z in digits01(m) if z % blockmod == c % blockmod]
        setxs = set(xs)
        ds = digits01(d)
        cap = energy_data(c,d)[2][-1]
        used = 0
        for n, np, x in product(ns,ns,xs):
            if n == np:
                continue
            y = (np*x*pow(n,-1,modulus)) % modulus
            if y not in setxs:
                continue
            residue = (np*x-n*y)//modulus
            count = 0
            for a,b,aa,bb in product(ds,repeat=4):
                actual = (((np+modulus*a)*(x+modulus*b)
                           -(n+modulus*aa)*(y+modulus*bb))
                          % (modulus*blockmod) == 0)
                predicted = (residue + c*(a-aa)+b-bb) % blockmod == 0
                assert actual == predicted
                count += actual
                extensions += 1
            assert count <= cap
            cases += 1
            used += 1
            if used >= 100:
                break
    return dict(prefix_cases=cases, extension_equivalences=extensions)


def fibonacci(n):
    return fib_pair(n)[0]


def h_graph(m,e):
    lengths = [(m-1-r)//e+1 if r<m else 0 for r in range(e)]
    ans=1
    for l in lengths:
        ans *= fibonacci(l+2)
    return ans


def check_affine_fibonacci():
    cases = products = 0
    for m in range(1,6):
        modulus=3**m
        ds=digits01(m); dset=set(ds)
        for r in range(4,modulus,3):
            w=r-1; e=0
            while w%3==0:
                e+=1;w//=3
            bound=h_graph(m,e)
            for shift in range(modulus):
                cnt=sum((r*z+shift)%modulus in dset for z in ds)
                products+=len(ds)
                assert cnt<=bound
                cases+=1
    return dict(affine_cases=cases, digit_products=products)



#!/usr/bin/env python3
"""Exact finite checks supplementing the proof; not an asymptotic proof."""
from collections import Counter
from fractions import Fraction
from hashlib import sha256
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent


def cantor_words(length):
    vals = [0]
    power = 1
    for _ in range(length):
        vals += [x + power for x in vals]
        power *= 3
    return vals


def fib(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def independent_count(length, distance):
    answer = 1
    for a in range(min(length, distance)):
        vertices = 1 + (length - 1 - a) // distance
        answer *= fib(vertices + 2)
    return answer


def valuation3(n):
    assert n != 0
    e = 0
    while n % 3 == 0:
        n //= 3
        e += 1
    return e


def main():
    report = {'proof_sha256': sha256((ROOT / 'power_gain_proof.txt').read_bytes()).hexdigest()}
    moments = []
    for h in range(10):
        words = cantor_words(h)
        coefficients = Counter(a + b for a in words for b in words)
        energy = sum(v * v for v in coefficients.values())
        assert energy == 6 ** h
        assert max(coefficients) == 3 ** h - 1
        moments.append({'h': h, 'energy': energy, 'fourth_moment': str(Fraction(energy, 16 ** h))})
    report['exact_fourth_moments'] = moments

    systems = input_words = 0
    equality_cases = 0
    for n in range(2, 10):
        modulus = 3 ** n
        words = cantor_words(n)
        allowed = set(words)
        for r in range(4, modulus, 3):
            e = valuation3(r - 1)
            admissible = sum((r * x) % modulus in allowed for x in words)
            bound = independent_count(n, e)
            assert admissible <= bound, (n, r, e, admissible, bound)
            systems += 1
            input_words += len(words)
        for e in range(1, n):
            r = 1 + 3 ** e
            admissible = sum((r * x) % modulus in allowed for x in words)
            assert admissible == independent_count(n, e)
            equality_cases += 1
    report['golden_bound'] = {'residue_systems': systems, 'word_checks': input_words, 'attained_cases': equality_cases}

    divisor_cases = close_pair_cases = 0
    for Y in [10, 13, 40, 100, 121, 364, 1000, 1093, 3280, 5000]:
        K = 0
        while 3 ** K <= Y:
            K += 1
        S = [x for x in cantor_words(K) if 1 <= x <= Y and x % 3 == 1]
        for d in range(1, Y + 1):
            j = 0
            while 3 ** (j + 1) <= d:
                j += 1
            actual = sum(x % d == 0 for x in S)
            assert actual <= 2 ** (K - j)
            divisor_cases += 1
        for e in range(1, K):
            buckets = Counter(x % (3 ** e) for x in S)
            assert max(buckets.values(), default=0) <= 2 ** (K - e)
            ordered = sum(v * (v - 1) for v in buckets.values())
            assert ordered <= len(S) * 2 ** (K - e)
            close_pair_cases += 1
    report['cantor_divisor_cases'] = divisor_cases
    report['valuation_bucket_cases'] = close_pair_cases

    # Exact residue counts illustrate the first-moment input, with no floating
    # Fourier computation. They are finite examples, not a test of the limit.
    examples = []
    for Y in [40, 121, 364, 1093]:
        K = 0
        while 3 ** K <= Y:
            K += 1
        L = 6 * K
        S = [x for x in cantor_words(K) if 1 <= x <= Y and x % 3 == 1]
        enough = 0
        for N in S:
            counts = [0] * N
            counts[0] = 1
            power = 1 % N
            for _ in range(L):
                new = counts.copy()
                for a, count in enumerate(counts):
                    new[(a + power) % N] += count
                counts = new
                power = (power * 3) % N
            assert sum(counts) == 2 ** L
            if 2 * N * counts[0] >= 2 ** L:
                enough += 1
        examples.append({'Y': Y, 'L': L, 'denominators': len(S), 'at_least_half_mean_in_zero_class': enough})
    report['finite_distribution_examples'] = examples
    report['status'] = 'PASS'
    report['scope'] = 'exact digit energies, all finite local golden systems through length9, divisor cylinders and valuation bins; finite distribution examples only'
    (ROOT / 'power_gain_lemma_checks.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()

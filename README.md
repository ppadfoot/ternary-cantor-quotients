# Integer quotients of ternary Cantor numbers: a power lower bound and an infinite exceptional family

**Timofei Iuzhakov** · Research preprint **1.0.0** · 6 November 2026

[Paper](paper/ternary_cantor_quotients.pdf) · [LaTeX](paper/ternary_cantor_quotients.tex) · [Versioned release](https://github.com/ppadfoot/ternary-cantor-quotients/releases/tag/v1.0.0) · [Citation](CITATION.cff)

The integer-multiplier counts M_C(X) and M_H(X) are bounded below by c X^beta for sufficiently large X, with beta=0.666058529778... . For every k>=0, 621*3^(4k)-20 is not a quotient of positive integers whose ternary digits are 0 and 1; these form an infinite sporadic exceptional family.

The manuscript does not resolve Erdős Problem 406, exclude 1 from E2, or prove countability of E2. The multiplier lower bound, where discussed, is not a bound on the number of exceptional powers of two.

## Scope

The two main theorems have independent proofs: Fourier and overlap estimates for the lower bound, and a symbolic reverse-carry invariant for the exceptional family. The latter is an all-parameter proof, not extrapolation of a finite scan. It is not a matching upper bound for the count.

## Reproduction

Python 3.10 or newer, standard library only, assertions enabled:

```bash
python3 run_all_checks.py
```

The finite programs test identities, algorithm invariants and the supplied certificate. They do not replace the general mathematical arguments. Results and execution logs are included. The final-source internal reviews and their scope are in `audit/`.

Build with Tectonic 0.17.0 (or a conventional LaTeX installation):

```bash
cd paper
tectonic ternary_cantor_quotients.tex
```

## Citation

Cite the exact manuscript version and relevant theorem. For the code, also identify the commit. No DOI or arXiv identifier is claimed.

```bibtex
@unpublished{iuzhakov2026cantorquotients,
  author = {Timofei Iuzhakov},
  title = {Integer quotients of ternary Cantor numbers: a power lower bound and an infinite exceptional family},
  year = {2026},
  note = {Version 1.0.0; research preprint},
  url = {https://github.com/ppadfoot/ternary-cantor-quotients/releases/tag/v1.0.0}
}
```

AI assistance was used for mathematical development, editing, code and internal review. Sole author: Timofei Iuzhakov. Internal reviews are not external peer review or proof-assistant verification; novelty and worldwide priority are not certified by GitHub timestamps.

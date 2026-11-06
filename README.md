# Ternary Cantor quotients: more representations, infinitely many exceptions

**Timofei Iuzhakov** · Research preprint · **Version 1.0.0 — 6 November 2026**

**Which integers are ratios of two positive integers whose base-3 digits are all 0 or 1? This paper proves a stronger power lower bound for how many integers have such a representation, and proves an explicit infinite family of exceptions proposed by Bai, Meleshko, Riasat and Shallit.**

[**Read the paper · 13 pages**](https://github.com/ppadfoot/ternary-cantor-quotients/releases/download/v1.0.0/ternary_cantor_quotients.pdf) · [Release and complete archive](https://github.com/ppadfoot/ternary-cantor-quotients/releases/tag/v1.0.0) · [LaTeX source](paper/ternary_cantor_quotients.tex) · [How to cite](#citation)

## Two main results at a glance

| Result | What the paper proves | Why it matters |
| --- | --- | --- |
| **More representable integers — Theorem 1.1** | At least $cX^{\beta}$ representable integers up to $X$ for all sufficiently large $X$, with $\beta=0.6660585297\ldots$. | Raises the elementary lower-bound exponent from $\log_3 2=0.6309297535\ldots$. The same bound holds for the number of positive-dimensional 3-adic Cantor intersections. |
| **Infinitely many sporadic exceptions — Theorem 1.2** | Every $621\cdot3^{4k}-20$, for $k\ge0$, is unrepresentable, despite passing the two standard elementary obstruction tests. | Proves the proposed family and answers the infinitude question in Bai, Meleshko, Riasat and Shallit's paper. |

Both results and their complete proofs first appear in this repository's **v1.0.0** manuscript. Their proof methods are independent: Fourier estimates and finite-word combinatorics for the first, an explicit carry invariant for the second.

## The problem, with an example

Write $\mathcal D^+$ for the positive integers with ternary digits **0 and 1**:

```math
\mathcal D^+=\{1,3,4,9,10,12,13,27,28,\ldots\}.
```

We ask which positive integers can be written as $M=b/a$ with $a,b\in\mathcal D^+$. The quotient itself may contain the digit 2. For example,

```math
7=\frac{28}{4}=\frac{(1001)_3}{(11)_3},
\qquad 7=(21)_3.
```

Thus division produces integers beyond the original digit set. How many additional integers can it produce? And which integers remain impossible?

Some literature defines Cantor integers using digits **0 and 2**. Those positive integers are exactly $2\mathcal D^+$, so their ratios give the same quotient problem.

## Result 1: a larger exponent for the counting problem

Let $M_C(X)$ count the positive integers $M\le X$ admitting such a representation. Taking denominator $a=1$ gives the immediate lower bound of order $X^s$, where $s=\log_3 2$.

Theorem 1.1 proves that there are constants $c>0$ and $X_0$ such that

```math
\boxed{M_C(X)\ge cX^{\beta}\quad(X\ge X_0),
\qquad\beta=0.666058529778\ldots>\log_3 2.}
```

The exponent is explicit. With $\varphi=(1+\sqrt5)/2$ and $g=\log_3\varphi$,

```math
\beta=s+(2s-1)\frac{s-g}{1+g}.
```

**Why this matters.** The improvement is in the power of $X$: the exponent increases by approximately **0.0351288**. The argument obtains many distinct quotients by varying the Cantor denominator and controlling how often different denominators produce the same integer.

There is also a fractal consequence. Let $\Sigma\subset\mathbb Z_3$ be the set of 3-adic integers with digits 0 and 1, and put

```math
C(1,M)=\{x\in\mathbb Z_3:x\in\Sigma,\ Mx\in\Sigma\}.
```

Every positive finite integer witness yields a positive-dimensional subset of $C(1,M)$ by repeating separated digit blocks. Consequently the count

```math
M_H(X)=\#\{1\le M\le X:\dim_H C(1,M)>0\}
```

also satisfies **$M_H(X)\ge cX^{\beta}$** for sufficiently large $X$.

These are improved lower bounds for the two counting questions in **Problems 1.10 and 1.11** of [Lagarias's journal paper](https://doi.org/10.1112/jlms/jdn080), called Problems 1 and 2 in its [arXiv version](https://arxiv.org/abs/math/0512006). The sharp growth rates remain open in this work.

**Where to read the proof:** **Sections 2–5**. Fourier sampling controls distribution over Cantor denominators; a Fibonacci bound controls finite-word overlaps; averaging the actual 3-adic distances gives the final counting estimate.

## Result 2: the proposed exceptional family works for every parameter

There are two easy ways to rule out a quotient: a restriction on its lowest nonzero ternary digit, and a restriction on its size coming from the leading digits. Bai, Meleshko, Riasat and Shallit found further exceptions that escape both tests. In [Section 1.4 of their 2022 paper](https://arxiv.org/abs/2202.13694), they asked whether there are infinitely many such **sporadic exceptions** and proposed the family below.

Theorem 1.2 proves

```math
\boxed{621\cdot3^{4k}-20\text{ is a sporadic exception for every integer }k\ge0.}
```

Its first members are **601, 50,281 and 4,074,361**. For every member, there are no positive $a,b\in\mathcal D^+$ with $b=(621\cdot3^{4k}-20)a$. Every member also avoids the two elementary obstruction classes. Hence the sporadic exceptional set is infinite.

**Why this matters.** This establishes the suggested family for all parameters and gives an affirmative answer to the infinitude question. The obstruction must use more of the digit arithmetic than the two elementary tests capture.

The proof rewrites a hypothetical representation as

```math
b+20a=23\cdot3^{4k+3}a.
```

The resulting digit recurrence has a finite carry range and a register storing earlier digits. An explicit set of states is closed under every valid predecessor step and separates the starting state from the state a positive representation would have to reach. The certificate has **$38k+50$ states for $k\ge1$**, with a separate **65-state** certificate for $k=0$.

**Where to read the proof:** **Sections 6–8**, especially **Proposition 7.1 and Tables 1–3**. Symbolic identities establish the certificate for every $k$; exact verification code checks the carry images and register identities.

## Scope and relation to the companion paper

The two theorems address abundance and explicit nonrepresentation within the same integer quotient problem. The power bound is a lower bound; the exceptional family does not classify all unrepresentable integers or determine their density. Failure to have a finite integer witness also does not imply that $C(1,M)$ has dimension zero.

Our [companion paper on Lagarias's exceptional sets](https://github.com/ppadfoot/lagarias-zero-dimension) studies repeated multiplication by powers of two and proves dimension results. This paper counts arbitrary integer multipliers and studies finite digit witnesses. Erdős Problem 406 and the assertion $1\notin E_2$ remain unresolved here.

## Paper, certificate and verification

| Resource | Contents |
| --- | --- |
| [Paper](paper/ternary_cantor_quotients.pdf) and [source](paper/ternary_cantor_quotients.tex) | Both complete proofs, the exact exponent and all three certificate tables |
| [Counting checks](code/verify_power_gain_lemmas.py) | Exact finite checks of digital energies, finite-word bounds and divisor/valuation estimates |
| [Parametric certificate](certificate/verify_parametric_certificate.py) | 18 symbolic row variants, 384 carry/digit choices, formal register identities and all 260 predecessor choices in the base case |
| [Independent symbolic check](certificate/hostile_symbolic_check.py) and [model verifier](certificate/history_model_verifier.py) | Additional checks of the exceptional-family certificate |
| [Recorded results](verification/combined_summary.json) and [internal reviews](audit/README.md) | Program outcomes, review scope and exact source hashes |
| [Version history](CHANGELOG.md) and [publication checklist](PUBLICATION_CHECKLIST.json) | The v1 manuscript contents and release checks |

Run all checks with **Python 3.10 or newer**, standard library only, with assertions enabled:

```bash
python3 run_all_checks.py
```

Build the paper with Tectonic 0.17.0:

```bash
cd paper
tectonic ternary_cantor_quotients.tex
```

Finite tests supplement the written proofs. The exceptional-family certificate uses exact symbolic identities for the parameter; numerical examples are additional checks. AI assistance was used in mathematical development, editing, code and internal review. The reviews are **not external peer review or proof-assistant verification**. Sole author: **Timofei Iuzhakov**.

## Citation

Cite **v1.0.0**, specifying **Theorem 1.1** for the power lower bound or **Theorem 1.2** for the infinite exceptional family. The [versioned release](https://github.com/ppadfoot/ternary-cantor-quotients/releases/tag/v1.0.0) fixes the paper and accompanying archive. The main README may receive explanatory updates between manuscript releases.

[CITATION.cff](CITATION.cff) and [CITATION.bib](CITATION.bib) provide the citation:

```bibtex
@unpublished{iuzhakov2026cantorquotients,
  author = {Timofei Iuzhakov},
  title = {Integer quotients of ternary Cantor numbers: a power lower bound and an infinite exceptional family},
  year = {2026},
  note = {Version 1.0.0; research preprint},
  url = {https://github.com/ppadfoot/ternary-cantor-quotients/releases/tag/v1.0.0}
}
```

For computational reproduction, also identify the code commit. No DOI or arXiv identifier has been assigned to this preprint.

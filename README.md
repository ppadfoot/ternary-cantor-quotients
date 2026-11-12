# Ternary Cantor quotients: more representations, infinitely many exceptions

**Timofei Iuzhakov** · Research preprint · **Version 3.0.0 — 12 November 2026**

**Which integers are ratios of two positive integers whose base-3 digits are all 0 or 1? This paper proves a stronger power lower bound for how many integers have such a representation, and proves an explicit infinite family of exceptions proposed by Bai, Meleshko, Riasat and Shallit.**

[**Read the current paper · 24 pages**](https://github.com/ppadfoot/ternary-cantor-quotients/releases/download/v3.0.0/ternary_cantor_quotients.pdf) · [v3 release and archive](https://github.com/ppadfoot/ternary-cantor-quotients/releases/tag/v3.0.0) · [Previous v2](https://github.com/ppadfoot/ternary-cantor-quotients/releases/tag/v2.0.0) · [LaTeX source](paper/ternary_cantor_quotients.tex) · [How to cite](#citation)

## What version 3 adds

**The same article, two complete new proof sections.** The title, sole author and citation key `iuzhakov2026cantorquotients` stay the same. All v1–v2 proofs remain included, and the counting exponent remains **0.691726633148796…**.

| New result | What is proved | Why it matters |
| --- | --- | --- |
| **Positive dimension for every sporadic-family member — Section 10** | Each $`M_k=621\cdot3^{4k}-20`$ has $`\dim_H C(1,M_k)\ge d_k>0`$, although none has a positive finite integer witness. | Completes the geometric picture of the family proved unrepresentable in v1: every member belongs to $`\mathcal M_H\setminus\mathcal M_C`$. |
| **Every representation of 289 is universal — Section 11** | If nonzero 0/1 polynomials satisfy $`P(3)=289Q(3)`$, then $`P(t)=(1-t^2-t^3+t^4+t^5)Q(t)`$. | Rules out all local representations of 289 and answers the corresponding question in Anders–Dawsey–Reznick–Sisneros-Thiry, arXiv v1. |
| **An explicit family of local representations — Section 11** | Every $`4\cdot3^k-2`$, $`k\ge1`$, has an explicit finite witness with $`k(k+1)+1`$ numerator digits; the constructed representation is local for $`k\ge2`$. | Provides a uniform construction contrasting with the rigidity of 289. No shortest-length or counting improvement is asserted. |

### 1. No finite witness, but a positive-dimensional intersection

The family already established in v1 has a stronger description in v3:

```math
\boxed{M_k\notin\mathcal M_C,\qquad\dim_H C(1,M_k)\ge d_k>0
\quad\text{for every }k\ge0.}
```

The lower bound is explicit. Let $`d_k`$ be the unique positive solution of

```math
3^{-m_kd_k}+3^{-L_kd_k}=1,\qquad
(m_0,L_0)=(3,12),\quad(m_k,L_k)=(4k+3,12k+6)\ (k\ge1).
```

**Why this matters.** A finite integer witness is sufficient for positive dimension, but it is not necessary. Strict inclusion was already known in the literature; v3 establishes this stronger description for **every member of the specific sporadic family**. The proof constructs a reachable carry and two return cycles with different first digits, producing a disjoint self-similar subset. Its dimension is exactly $`d_k`$; the full intersection is only proved to have dimension **at least** $`d_k`$.

### 2. A complete answer for the representations of 289

A representation is **universal** when its denominator polynomial divides its numerator polynomial; otherwise it is **local**. Version 3 proves

```math
\boxed{P(3)=289Q(3)\quad\Longrightarrow\quad
P(t)=(1-t^2-t^3+t^4+t^5)Q(t).}
```

This is not vacuous: $`289=80920/280`$, and both numerator and denominator have only ternary digits 0 and 1.

**Why this matters.** The table in §4 of [Anders–Dawsey–Reznick–Sisneros-Thiry, arXiv:2308.07252v1](https://arxiv.org/abs/2308.07252v1) leaves local representations of 289 as a question. Our theorem covers **all finite representations**, not only indecomposable ones. A complete carry graph and polynomial potentials prove the assertion for arbitrary word length. The certificate verifies polynomial coefficients, not merely equality after substituting $`t=3`$.

[New proof sections](paper/) · [Version-3 source map and independent internal reviews](audit/v3/README.md) · [Exact verification code](code/v3/) · [Version history](CHANGELOG.md)

## What version 2 added

**The same article, a stronger counting theorem.** The title, sole author and citation key `iuzhakov2026cantorquotients` are retained. The original exceptional-family theorem and its complete proof are unchanged.

| Version | Counting lower bound | First appearance |
| --- | --- | --- |
| **v1.0.0** | $`M_C(X)\gg X^{0.6660585297\ldots}`$ | Theorem 1.1; 6 November 2026 |
| **v2.0.0** | $`M_C(X)\gg X^{\beta_*}`$, $`\beta_*=(1+s)^2/(7-5s)=0.691726633148796\ldots`$, $`s=\log_3 2`$ | **Theorem 9.1**; 8 November 2026 |

**The exact exponent is attained, without an epsilon loss.** Section 9 supplies the full proof: an endpoint mean-discrepancy estimate, an affine Fibonacci bound valid after fixing prefixes, and an exact 113-state energy certificate for the fixed residue class $`112\pmod{3^{128}}`$. Together they control both the number of representations and collisions between them. The exponent increases by approximately **0.0256681** over v1.

This strengthens the lower bound in Lagarias's finite-quotient counting problem (journal Problem 1.10). It does **not** determine the sharp growth rate or prove Erdős Problem 406. The block length is fixed before the limit; the implicit constants and threshold may be very large.

[Original v1 release](https://github.com/ppadfoot/ternary-cantor-quotients/releases/tag/v1.0.0) · [Full version history](CHANGELOG.md) · [New proof source](paper/endpoint_bound.tex) · [Exact checks](code/endpoint/) · [Focused internal review](audit/v2/integration_review.txt)

## Results introduced in version 1

The following results and their original numbering are preserved. Theorem 9.1 above strengthens the counting exponent of Theorem 1.1.


| Result | What the paper proves | Why it matters |
| --- | --- | --- |
| **More representable integers — Theorem 1.1** | At least $`cX^{\beta}`$ representable integers up to $`X`$ for all sufficiently large $`X`$, with $`\beta=0.6660585297\ldots`$. | Raises the elementary lower-bound exponent from $`\log_3 2=0.6309297535\ldots`$. The same bound holds for the number of positive-dimensional 3-adic Cantor intersections. |
| **Infinitely many sporadic exceptions — Theorem 1.2** | Every $`621\cdot3^{4k}-20`$, for $`k\ge0`$, is unrepresentable, despite passing the two standard elementary obstruction tests. | Proves the proposed family and answers the infinitude question in Bai, Meleshko, Riasat and Shallit's paper. |

Both results and their complete proofs first appear in this repository's **v1.0.0** manuscript. Their proof methods are independent: Fourier estimates and finite-word combinatorics for the first, an explicit carry invariant for the second.

## The problem, with an example

Write $`\mathcal D^+`$ for the positive integers with ternary digits **0 and 1**:

```math
\mathcal D^+=\{1,3,4,9,10,12,13,27,28,\ldots\}.
```

We ask which positive integers can be written as $`M=b/a`$ with $`a,b\in\mathcal D^+`$. The quotient itself may contain the digit 2. For example,

```math
7=\frac{28}{4}=\frac{(1001)_3}{(11)_3},
\qquad 7=(21)_3.
```

Thus division produces integers beyond the original digit set. How many additional integers can it produce? And which integers remain impossible?

Some literature defines Cantor integers using digits **0 and 2**. Those positive integers are exactly $`2\mathcal D^+`$, so their ratios give the same quotient problem.

## The original v1 counting argument (retained)

Let $`M_C(X)`$ count the positive integers $`M\le X`$ admitting such a representation. Taking denominator $`a=1`$ gives the immediate lower bound of order $`X^s`$, where $`s=\log_3 2`$.

Theorem 1.1 proves that there are constants $`c>0`$ and $`X_0`$ such that

```math
\boxed{M_C(X)\ge cX^{\beta}\quad(X\ge X_0),
\qquad\beta=0.666058529778\ldots>\log_3 2.}
```

The exponent is explicit. With $`\varphi=(1+\sqrt5)/2`$ and $`g=\log_3\varphi`$,

```math
\beta=s+(2s-1)\frac{s-g}{1+g}.
```

**Why this matters.** The improvement is in the power of $`X`$: the exponent increases by approximately **0.0351288**. The argument obtains many distinct quotients by varying the Cantor denominator and controlling how often different denominators produce the same integer.

There is also a fractal consequence. Let $`\Sigma\subset\mathbb Z_3`$ be the set of 3-adic integers with digits 0 and 1, and put

```math
C(1,M)=\{x\in\mathbb Z_3:x\in\Sigma,\ Mx\in\Sigma\}.
```

Every positive finite integer witness yields a positive-dimensional subset of $`C(1,M)`$ by repeating separated digit blocks. Consequently the count

```math
M_H(X)=\#\{1\le M\le X:\dim_H C(1,M)>0\}
```

also satisfies **$`M_H(X)\ge cX^{\beta}`$** for sufficiently large $`X`$.

These are improved lower bounds for the two counting questions in **Problems 1.10 and 1.11** of [Lagarias's journal paper](https://doi.org/10.1112/jlms/jdn080), called Problems 1 and 2 in its [arXiv version](https://arxiv.org/abs/math/0512006). The sharp growth rates remain open in this work.

**Where to read the proof:** **Sections 2–5**. Fourier sampling controls distribution over Cantor denominators; a Fibonacci bound controls finite-word overlaps; averaging the actual 3-adic distances gives the final counting estimate.

## The exceptional-family theorem (retained)

There are two easy ways to rule out a quotient: a restriction on its lowest nonzero ternary digit, and a restriction on its size coming from the leading digits. Bai, Meleshko, Riasat and Shallit found further exceptions that escape both tests. In [Section 1.4 of their 2022 paper](https://arxiv.org/abs/2202.13694), they asked whether there are infinitely many such **sporadic exceptions** and proposed the family below.

Theorem 1.2 proves

```math
\boxed{621\cdot3^{4k}-20\text{ is a sporadic exception for every integer }k\ge0.}
```

Its first members are **601, 50,281 and 4,074,361**. For every member, there are no positive $`a,b\in\mathcal D^+`$ with $`b=(621\cdot3^{4k}-20)a`$. Every member also avoids the two elementary obstruction classes. Hence the sporadic exceptional set is infinite.

**Why this matters.** This establishes the suggested family for all parameters and gives an affirmative answer to the infinitude question. The obstruction must use more of the digit arithmetic than the two elementary tests capture.

The proof rewrites a hypothetical representation as

```math
b+20a=23\cdot3^{4k+3}a.
```

The resulting digit recurrence has a finite carry range and a register storing earlier digits. An explicit set of states is closed under every valid predecessor step and separates the starting state from the state a positive representation would have to reach. The certificate has **$`38k+50`$ states for $`k\ge1`$**, with a separate **65-state** certificate for $`k=0`$.

**Where to read the proof:** **Sections 6–8**, especially **Proposition 7.1 and Tables 1–3**. Symbolic identities establish the certificate for every $`k`$; exact verification code checks the carry images and register identities.

## Related results in the dimension manuscript

The [dimension article, v3.0.0](https://github.com/ppadfoot/lagarias-zero-dimension/releases/tag/v3.0.0), Theorem 14.1, proved

```math
M_H(X)\asymp X,\qquad
\#((\mathcal M_H\setminus\mathcal M_C)\cap[1,X])\gg X.
```

This determines the linear order in Lagarias's second counting problem and shows that finite integer witnesses omit linearly many positive-dimensional intersections. The proof uses summable rational Cantor denominators and a divisibility sieve.

These results first appeared in the dimension article, cited as `iuzhakov2026lagarias`, v3.0.0, and are retained in [its current v4](https://github.com/ppadfoot/lagarias-zero-dimension/releases/tag/v4.0.0). They are distinct from the improved finite-quotient bound in this article's v2.0.0. The exact multiplier asymptotic, the sharp finite-quotient count and Erdős Problem 406 remain open.

## Scope and relation to the companion paper

The article connects abundance, explicit nonrepresentation, positive-dimensional intersections and the polynomial structure of finite witnesses. The power bound is a lower bound; the exceptional family does not classify all unrepresentable integers or determine their density. Version 3 proves this distinction throughout the sporadic family, with a quantitative dimension lower bound.

Our [companion paper on Lagarias's exceptional sets](https://github.com/ppadfoot/lagarias-zero-dimension) studies repeated multiplication by powers of two and proves dimension results. This paper counts arbitrary integer multipliers and studies finite digit witnesses. Erdős Problem 406 and the assertion $`1\notin E_2`$ remain unresolved here.

## Paper, certificate and verification

| Resource | Contents |
| --- | --- |
| [Paper](paper/ternary_cantor_quotients.pdf) and [source](paper/ternary_cantor_quotients.tex) | Complete v3 article: all v1–v2 proofs, plus positive dimension and universal/local representations in Sections 10–11 |
| [Counting checks](code/verify_power_gain_lemmas.py) | Exact finite checks of digital energies, finite-word bounds and divisor/valuation estimates |
| [Parametric certificate](certificate/verify_parametric_certificate.py) | 18 symbolic row variants, 384 carry/digit choices, formal register identities and all 260 predecessor choices in the base case |
| [Independent symbolic check](certificate/hostile_symbolic_check.py) and [model verifier](certificate/history_model_verifier.py) | Additional checks of the exceptional-family certificate |
| [New v3 checks](code/v3/) | Exact symbolic cycle identities, the full 289 carry graph and coefficient-level polynomial potentials, plus finite local-family tests |
| [Recorded results](verification/combined_summary.json) and [internal reviews](audit/README.md) | Program outcomes, review scope and exact source hashes |
| [Version history](CHANGELOG.md) and [publication checklist](PUBLICATION_CHECKLIST.json) | Versioned manuscript contents and release checks |

Run all checks with **Python 3.10 or newer**, standard library only, with assertions enabled:

```bash
python3 run_all_checks.py
```

Build the paper with Tectonic 0.17.0:

```bash
cd paper
tectonic ternary_cantor_quotients.tex
```

The full v3 run includes the five retained verification programs and two new programs. The two new proof sections receive independent internal cross-reviews, with a separate critical review of the integrated claims and attribution. Earlier review files retain their original scope. Finite tests supplement the written proofs. The exceptional-family certificate uses exact symbolic identities for the parameter; numerical examples are additional checks. AI assistance was used in mathematical development, editing, code and internal review. The reviews are **not external peer review or proof-assistant verification**. Sole author: **Timofei Iuzhakov**.

## Citation

**Keep the citation key `iuzhakov2026cantorquotients` and specify the version.** Cite **v2.0.0, Theorem 9.1**, for the exponent 0.691726633148796…; cite **v1.0.0, Theorem 1.1**, for the original exponent. The exceptional-family theorem remains Theorem 1.2. Cite **v3.0.0, Sections 10–11**, for the new positive-dimension and universal/local representation results. Each versioned release fixes its own PDF and archive; the main README can receive explanatory updates.

[CITATION.cff](CITATION.cff) and [CITATION.bib](CITATION.bib) provide the citation:

```bibtex
@unpublished{iuzhakov2026cantorquotients,
  author = {Timofei Iuzhakov},
  title = {Integer quotients of ternary Cantor numbers: a power lower bound and an infinite exceptional family},
  year = {2026},
  note = {Version 3.0.0; research preprint},
  url = {https://github.com/ppadfoot/ternary-cantor-quotients/releases/tag/v3.0.0}
}
```

For computational reproduction, also identify the code commit. No DOI or arXiv identifier has been assigned to this preprint.



# Manuscript versions

## v2.0.0 — 8 November 2026

Updated version of the same article, **Integer quotients of ternary Cantor numbers: a power lower bound and an infinite exceptional family**, by **Timofei Iuzhakov**. Citation key: `iuzhakov2026cantorquotients`.

- **Theorem 9.1:** improves the finite-quotient lower-bound exponent from 0.6660585297… to 0.691726633148796…, with no epsilon loss.
- New Section 9 proves the endpoint mean-discrepancy estimate, affine tail bound, fixed-class block-energy estimate, and final counting argument.
- Includes the exact 113-state certificate and a focused reproducible checker. All five verification programs pass.
- Original Sections 2–8 are retained byte for byte; Theorems 1.1 and 1.2 keep their numbering. The abstract and introduction identify the stronger result.
- Focused internal review of the new English section, independently recomputed energy and sign inequalities, PDF inspection and fixed release archive. No external peer review or exhaustive priority claim.

[PDF](https://github.com/ppadfoot/ternary-cantor-quotients/releases/download/v2.0.0/ternary_cantor_quotients.pdf) · [Release](https://github.com/ppadfoot/ternary-cantor-quotients/releases/tag/v2.0.0)

The v1 release is preserved. The sharp finite-quotient count and Erdős Problem 406 remain open. The separate linear-order result for positive-dimensional intersections belongs to the dimension manuscript v3, not to this new theorem.

## v1.0.0 — 6 November 2026

**Integer quotients of ternary Cantor numbers: a power lower bound and an infinite exceptional family**  
Timofei Iuzhakov · 13 pages

[Paper](https://github.com/ppadfoot/ternary-cantor-quotients/releases/download/v1.0.0/ternary_cantor_quotients.pdf) · [Release and complete archive](https://github.com/ppadfoot/ternary-cantor-quotients/releases/tag/v1.0.0)

This first manuscript release contains two main results with independent complete proofs.

### Theorem 1.1 — a power lower bound

The number $M_C(X)$ of positive integer quotients of finite ternary 0/1-digit integers up to $X$ satisfies

$$
M_C(X)\ge cX^{\beta},\qquad \beta=0.666058529778\ldots,
$$

for some constant $c>0$ and all sufficiently large $X$. The same bound holds for $M_H(X)$, the number of multipliers producing positive-dimensional 3-adic Cantor intersections.

The exponent exceeds the elementary exponent $\log_3 2=0.630929753571\ldots$, improving the lower bounds in Lagarias's Problems 1.10 and 1.11. Sections 2–5 give the Fourier, divisor, finite-word overlap and counting arguments.

### Theorem 1.2 — an infinite sporadic exceptional family

For every integer $k\ge0$, the integer $621\cdot3^{4k}-20$ is not a quotient of two positive finite ternary 0/1-digit integers and lies outside the two elementary obstruction classes. This proves that the sporadic exceptional set of Bai, Meleshko, Riasat and Shallit is infinite and establishes their proposed family.

Sections 6–8 give the delayed carry model, the complete symbolic certificate with $38k+50$ states for $k\ge1$, and a separate 65-state base certificate for $k=0$. All three certificate tables are included.

### Accompanying materials

The release includes the PDF, LaTeX source, exact verification code, formal-parameter certificate checks, additional independent checks, final-source internal review reports, citation files and SHA-256 checksums. Finite computations supplement the mathematical proofs; the reviews are internal AI-assisted reviews.

The sharp counting asymptotics, a classification of all exceptional integers and Erdős Problem 406 remain outside these conclusions. Dimension results for repeated powers of two are published separately in the [companion repository](https://github.com/ppadfoot/lagarias-zero-dimension).


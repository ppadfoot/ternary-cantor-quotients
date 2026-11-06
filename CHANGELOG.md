# Manuscript versions

Each manuscript release fixes the paper, source, verification code and review record. The main README explains the results and may be updated independently of manuscript versions.

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

# Validation of the amortized posterior

## SBC on 1000 held-out simulations, 500 posterior draws each

| parameter | 50 % coverage | 90 % coverage | max |ECDF − uniform| | posterior mean r | mean 90 % width | prior 90 % width |
|---|---|---|---|---|---|---|
| delta_deg | 0.51 | 0.94 | 0.026 | +0.746 | 14.500 | 27.000 |
| scale | 0.50 | 0.94 | 0.032 | +0.873 | 0.123 | 0.270 |
| c_n | 0.51 | 0.93 | 0.024 | +0.906 | 0.228 | 0.720 |
| c_e | 0.52 | 0.92 | 0.037 | +0.902 | 0.222 | 0.720 |
| log10_sigma_v | 0.52 | 0.93 | 0.037 | +0.990 | 0.210 | 1.529 |

Reference: for 1000 draws the 95 % critical value of the max ECDF deviation is 0.043.

## Posterior on the real star windows (120 s, stride 30 s) vs least-squares reference

Reference (all-leg fit): δ=+0.09°, s=0.965, c=(+0.003,-0.019) m/s (no like-for-like reference for σ_v)

| parameter | median of posterior means | median 90 % interval | windows whose 90 % interval contains the reference |
|---|---|---|---|
| delta_deg | -0.554 | [-1.508, +0.419] | 52 % (12/23); mean bias -0.659, median |z| 1.6 |
| scale | +0.972 | [+0.952, +0.991] | 65 % (15/23); mean bias -0.000, median |z| 0.9 |
| c_n | -0.004 | [-0.026, +0.012] | 78 % (18/23); mean bias -0.014, median |z| 0.8 |
| c_e | -0.031 | [-0.059, -0.010] | 52 % (12/23); mean bias -0.007, median |z| 1.5 |
| log10_sigma_v | -1.816 | [-2.029, -1.624] | no reference |

Windows with heading span < 20°: 1; with a turn: 22.
| group | n | 90 % width δ [°] | 90 % width |c| [m/s] | 90 % width s |
|---|---|---|---|---|
| straight | 1 | 1.95 | 0.189 | 0.221 |
| with turn | 22 | 1.91 | 0.064 | 0.069 |

## Posterior-predicted vs observed 2-min dead-reckoning drift (star windows)

- Observed nominal-DR drift after 120 s: median 4.8 m (range 1.0–13.1).
- Posterior-predicted drift: median of window medians 4.6 m; observed drift inside the 90 % predictive interval in 65 % of windows.
- Correlation observed vs predicted median across windows: +0.44.

## Posterior on Thor's 6 surface windows vs Thor's own surface fit

Reference (Thor surface fit, δ and c confounded): δ=-3.91°, s=0.984, c=(-0.053,-0.058)

| parameter | median of posterior means | median 90 % interval | windows containing the reference |
|---|---|---|---|
| delta_deg | -5.129 | [-15.139, +4.900] | 67 % |
| scale | +0.981 | [+0.855, +1.117] | 100 % |
| c_n | -0.007 | [-0.323, +0.292] | 67 % |
| c_e | -0.060 | [-0.326, +0.262] | 100 % |
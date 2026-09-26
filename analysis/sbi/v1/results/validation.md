# Validation of the amortized posterior

## SBC on 1000 held-out simulations, 500 posterior draws each

| parameter | 50 % coverage | 90 % coverage | max |ECDF − uniform| | posterior mean r | mean 90 % width | prior 90 % width |
|---|---|---|---|---|---|---|
| delta_deg | 0.49 | 0.94 | 0.026 | +0.738 | 14.171 | 27.000 |
| scale | 0.50 | 0.91 | 0.023 | +0.860 | 0.128 | 0.270 |
| c_n | 0.49 | 0.92 | 0.047 | +0.916 | 0.223 | 0.720 |
| c_e | 0.53 | 0.93 | 0.026 | +0.902 | 0.222 | 0.720 |
| log10_sigma_v | 0.53 | 0.91 | 0.049 | +0.997 | 0.081 | 0.900 |

Reference: for 1000 draws the 95 % critical value of the max ECDF deviation is 0.043.

## Posterior on the real star windows (120 s, stride 30 s) vs least-squares reference

Reference (all-leg fit): δ=+0.09°, s=0.965, c=(+0.003,-0.019) m/s, log10σ=-0.77

| parameter | median of posterior means | median 90 % interval | windows whose 90 % interval contains the reference |
|---|---|---|---|
| delta_deg | -1.044 | [-1.619, -0.463] | 22 % (5/23) |
| scale | +0.975 | [+0.956, +0.994] | 70 % (16/23) |
| c_n | +0.011 | [-0.004, +0.032] | 57 % (12/23) |
| c_e | -0.034 | [-0.053, -0.010] | 61 % (14/23) |
| log10_sigma_v | -1.221 | [-1.272, -1.174] | 0 % (0/23) |

Windows with heading span < 20°: 1; with a turn: 22.
| group | n | 90 % width δ [°] | 90 % width |c| [m/s] | 90 % width s |
|---|---|---|---|---|
| straight | 1 | 1.36 | 0.151 | 0.202 |
| with turn | 22 | 1.16 | 0.058 | 0.066 |

## Posterior-predicted vs observed 2-min dead-reckoning drift (star windows)

- Observed nominal-DR drift after 120 s: median 4.8 m (range 1.0–13.1).
- Posterior-predicted drift: median of window medians 5.8 m; observed drift inside the 90 % predictive interval in 74 % of windows.
- Correlation observed vs predicted median across windows: +0.58.

## Posterior on Thor's 6 surface windows vs Thor's own surface fit

Reference (Thor surface fit, δ and c confounded): δ=-3.91°, s=0.984, c=(-0.053,-0.058)

| parameter | median of posterior means | median 90 % interval | windows containing the reference |
|---|---|---|---|
| delta_deg | -4.596 | [-14.275, +5.156] | 50 % |
| scale | +0.970 | [+0.853, +1.087] | 67 % |
| c_n | -0.015 | [-0.332, +0.285] | 50 % |
| c_e | -0.098 | [-0.331, +0.184] | 67 % |
| log10_sigma_v | -1.244 | [-1.303, -1.185] | 0 % |
# Misspecification detection (Mahalanobis distance in summary space)

Summary dimension 32; null d² from 2000 held-out simulations: median 30.5, 99th percentile (threshold) 62.2.

| window set | n | median d² | flagged (d² > threshold) | 90 % coverage of reference, unflagged | flagged |
|---|---|---|---|---|---|
| star | 23 | 28.4 | 0 % | 39 % (δ: 17 %) | nan % (δ: nan %) |
|  | | | | posterior δ median -1.01° [-1.67, -0.44] vs reference +0.09° | |
| sidescan_dive | 64 | 28.8 | 0 % | 66 % (δ: 100 %) | nan % (δ: nan %) |
|  | | | | posterior δ median +0.50° [-13.98, +14.66] vs reference +0.09° | |
| thor_surface | 6 | 51.3 | 33 % | 70 % (δ: 75 %) | 0 % (δ: 0 %) |
|  | | | | posterior δ median -6.68° [-14.00, +4.85] vs reference -3.91° | |
| thor_dive | 79 | 36.5 | 3 % | 80 % (δ: 100 %) | 80 % (δ: 100 %) |
|  | | | | posterior δ median +0.72° [-13.50, +14.67] vs reference -3.91° | |
| star_raw | 23 | 31.0 | 0 % | 44 % (δ: 17 %) | nan % (δ: nan %) |
|  | | | | posterior δ median +11.03° [+10.37, +11.92] vs reference +12.81° | |

Coverage = fraction of (window, parameter) pairs whose 90 % interval contains the reference value; 'δ:' the same for the heading bias only.
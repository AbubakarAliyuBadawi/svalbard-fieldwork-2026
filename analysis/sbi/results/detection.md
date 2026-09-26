# Misspecification detection (Mahalanobis distance in summary space)

Summary dimension 32; null d² from 2000 held-out simulations: median 31.1, 99th percentile (threshold) 61.6.

| window set | n | median d² | flagged (d² > threshold) | 90 % coverage of reference, unflagged | flagged |
|---|---|---|---|---|---|
| star | 23 | 25.2 | 0 % | 63 % (δ: 57 %) | nan % (δ: nan %) |
|  | | | | posterior δ median -0.55° [-1.58, +0.29] vs reference +0.09° | |
| sidescan_dive | 64 | 31.5 | 0 % | 85 % (δ: 100 %) | nan % (δ: nan %) |
|  | | | | posterior δ median +0.40° [-13.61, +14.32] vs reference +0.09° | |
| thor_surface | 6 | 45.7 | 17 % | 90 % (δ: 80 %) | 50 % (δ: 0 %) |
|  | | | | posterior δ median -5.16° [-15.17, +5.37] vs reference -3.91° | |
| thor_dive | 79 | 28.8 | 0 % | 100 % (δ: 100 %) | nan % (δ: nan %) |
|  | | | | posterior δ median +0.31° [-14.27, +14.69] vs reference -3.91° | |
| star_raw | 23 | 34.3 | 0 % | 64 % (δ: 61 %) | nan % (δ: nan %) |
|  | | | | posterior δ median +12.09° [+11.01, +13.04] vs reference +12.81° | |

Coverage = fraction of (window, parameter) pairs whose 90 % interval contains the reference value; 'δ:' the same for the heading bias only.
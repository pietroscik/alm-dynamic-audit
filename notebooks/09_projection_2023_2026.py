#!/usr/bin/env python3
"""09 — Proiezione statico vs dinamico 2021-2026 su curve EIOPA EUR [O, verified].

Riproduce data/processed/backtest_static_vs_dynamic_2021_2026.csv:
- statico: curva congelata 31.12.2021 (r10 = 0.00205)
- dinamico: r10 effettivo per data
- repricing zero-coupon 10y su capitale 100
- lapse: q_t = q_{t-1} * exp(gamma * max(0, ds_{t-1}/10000)), gamma in [19.7, 30.1], lag 1
"""
import csv, math
from pathlib import Path

R10 = {  # no-VA, 10y spot, [O] EIOPA EUR (doclib 01a0c505, quality verified)
    "2021-12-31": 0.00205, "2022-12-31": 0.03092, "2023-01-31": 0.02764,
    "2024-01-31": 0.02472, "2025-01-31": 0.02333, "2026-01-31": 0.02798,
}
VA_BPS = {"2021-12-31": 3, "2022-12-31": 19, "2023-01-31": 17, "2024-01-31": 20, "2025-01-31": 20, "2026-01-31": 12}
STATIC_R10 = R10["2021-12-31"]
GAMMA_BAND = (19.7, 30.1)


def p10(r): return 100 / (1 + r) ** 10


def main():
    out = Path("data/processed/backtest_static_vs_dynamic_2021_2026.csv")
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["date", "r10_no_va_pct", "va_bps", "p10_dyn_eur", "p10_static_eur", "gap_static_minus_dyn_eur", "tag"])
        for d, r in R10.items():
            w.writerow([d, round(r * 100, 3), VA_BPS[d], round(p10(r), 2), round(p10(STATIC_R10), 2),
                        round(p10(r) - p10(STATIC_R10), 2), "O-curve/E-derived-repricing"])
    # lapse projection 2023 (lag-1 sul widening 2022 di 76 bps [O])
    q0 = 3.5  # avg-reserves 2022 [O]
    for g in GAMMA_BAND:
        print(f"gamma={g}: q_2023 = {q0 * math.exp(g * 0.0076):.2f}% (osservato 4.4% [O])")
    print("2024-2026: spread n.d. -> floor attivo, q resta al livello 2023 (isteresi [E-model])")


if __name__ == "__main__":
    main()

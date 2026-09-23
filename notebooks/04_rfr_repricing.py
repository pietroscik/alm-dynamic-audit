#!/usr/bin/env python3
"""
04_rfr_repricing.py — Riprezzamento reale del backtest statico vs dinamico.

Calcola dal dato [O] (data/processed/rfr_curves_eur_2021_2022.csv):
  1. VA per data (atteso piatto: 3/14/17/19 bps)
  2. Shifts reali vs 31/12/2021 (no_VA e with_VA, bps)
  3. Riprezzamento duration-based di BEL e attivi (sostituisce lo shift [E] +250bp)
  4. Duration implicite dalle disclosure VA di S.22.01.21/22 (finding DPHB)

Input [O] hardcoded con tracciabilità (EUR k):
  - BEL PV_GROUP 2021 = 151.468.375 (SFCR 2021 EN, S.22.01.21)
  - BEL PV_GROUP 2022 = 128.350.704 (Relazione Unica 2022, D.2)
  - TP 2021 = 151.694.417 / TP 2022 = 133.029.385 (idem)
  - Investimenti 2021 = 150.845.818 (SFCR 2021, S.02.01.02)
  - Impatto VA->0 su TP: 2021 = 217.453 (S.22.01.22 2021); 2022 = 565.931 (RU 2022)
Derivazioni [E-derived]: D_L = 5,30 e D_A = 4,94 (notebook backtest_2022_static_vs_dynamic.md).
"""
from __future__ import annotations

from pathlib import Path

import polars as pl

REPO = Path(__file__).resolve().parents[1]
CURVES = REPO / "data" / "processed" / "rfr_curves_eur_2021_2022.csv"

# [O] tracciati (EUR k)
BEL_21, BEL_22 = 151_468_375, 128_350_704
TP_21, TP_22 = 151_694_417, 133_029_385
INV_21 = 150_845_818
VA_TP_IMPACT = {"2021-12-31": 217_453, "2022-12-31": 565_931}
# [E-derived]
D_L, D_A = 5.30, 4.94

K = 1_000_000  # EUR k -> mld EUR


def main() -> None:
    df = pl.read_csv(CURVES).filter(pl.col("quality") == "verified")

    print("== 1. VA per data (atteso: piatto 3/14/17/19 bps) ==")
    va = (
        df.group_by("ref_date")
        .agg(pl.col("va_bps").min().alias("min"), pl.col("va_bps").max().alias("max"), pl.len().alias("n"))
        .sort("ref_date")
    )
    print(va)
    assert (va["min"] == va["max"]).all(), "VA non piatto: dato sospetto!"

    print("\n== 2. Shifts reali vs 31/12/2021 (bps) ==")
    piv = df.pivot(on="maturity", index=["ref_date", "sheet"], values="rate").sort(["sheet", "ref_date"])
    mats = [str(m) for m in range(1, 21)]
    base = {
        s: {m: piv.filter((pl.col("ref_date") == "2021-12-31") & (pl.col("sheet") == s))[m][0] for m in mats}
        for s in ("no_VA", "with_VA")
    }
    shifts = []
    for date in ("2022-05-31", "2022-09-30", "2022-12-31"):
        for s in ("no_VA", "with_VA"):
            row = piv.filter((pl.col("ref_date") == date) & (pl.col("sheet") == s))
            sh = [(row[m][0] - base[s][m]) * 10_000 for m in mats]
            shifts.append({
                "ref_date": date, "sheet": s,
                "n2_bps": round(sh[1]), "n10_bps": round(sh[9]), "n20_bps": round(sh[19]),
                "avg_bps": round(sum(sh) / 20, 1),
            })
    print(pl.DataFrame(shifts))

    print("\n== 3. Riprezzamento duration-based (sostituisce [E] +250bp) ==")
    avg_bps = next(r["avg_bps"] for r in shifts if r["ref_date"] == "2022-12-31" and r["sheet"] == "with_VA")
    dy = avg_bps / 10_000  # shift medio in decimale
    d_bel_rate = -D_L * (BEL_21 / K) * dy        # mld EUR
    d_assets = D_A * (INV_21 / K) * dy           # mld EUR
    d_bel_obs = (BEL_22 - BEL_21) / K            # mld EUR
    print(f"shift medio with_VA 2021->2022  : +{avg_bps:.1f} bps (vs [E] +250bp)")
    print(f"dBEL solo-tasso [E-derived]      : {d_bel_rate:+.2f} mld EUR")
    print(f"dBEL osservato [O]               : {d_bel_obs:+.2f} mld EUR")
    print(f"residuo non-tasso                 : {d_bel_obs - d_bel_rate:+.2f} mld EUR (runoff, nuovi affari, DPHB)")
    print(f"dAssets [E-derived]              : {d_assets:+.2f} mld EUR")
    print(f"contributo dinamico netto         : {d_assets + d_bel_rate:+.2f} mld EUR (era +1,41 con [E] +250bp)")

    print("\n== 4. Duration implicite dal VA (finding DPHB) ==")
    for date, tp in (("2021-12-31", TP_21), ("2022-12-31", TP_22)):
        va_bps = int(df.filter(pl.col("ref_date") == date)["va_bps"][0])
        d_impl = VA_TP_IMPACT[date] / (tp * va_bps / 10_000)
        print(f"{date}: VA {va_bps} bps, impatto VA->0 su TP {VA_TP_IMPACT[date]:,} k su TP {tp:,} k -> D implicita {d_impl:.2f}")
    print("\nD implicita 2021 (~4,8) coerente con D_L=5,30; 2022 (~2,2) NO: assorbimento DPHB.")


if __name__ == "__main__":
    main()

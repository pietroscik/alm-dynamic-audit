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

# [O] tracciati
BEL_21, BEL_22 = 151_468_375, 128_350_704
TP_21, TP_22 = 151_694_417, 133_029_385
INV_21 = 150_845_818
VA_TP_IMPACT = {"2021-12-31": 217_453, "2022-12-31": 565_931}
# [E-derived]
D_L, D_A = 5.30, 4.94


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
    base = {s: piv.filter((pl.col("ref_date") == "2021-12-31") & (pl.col("sheet") == s)) for s in ("no_VA", "with_VA")}
    shifts = []
    for date in ("2022-05-31", "2022-09-30", "2022-12-31"):
        for s in ("no_VA", "with_VA"):
            row = piv.filter((pl.col("ref_date") == date) & (pl.col("sheet") == s))
            sh = [(row[m][0] - base[s][m][0]) * 10_000 for m in map(str, range(1, 21))]
            shifts.append({"ref_date": date, "sheet": s, "n2": round(sh[1], 0), "n10": round(sh[9], 0),
                           "n20": round(sh[19], 0), "avg": round(sum(sh) / 20, 1)})
    print(pl.DataFrame(shifts))

    print("\n== 3. Riprezzamento duration-based (sostituisce [E] +250bp) ==")
    avg_sh_wva = next(r["avg"] for r in shifts if r["ref_date"] == "2022-12-31" and r["sheet"] == "with_VA") / 100
    d_bel_rate = -D_L * BEL_21 * avg_sh_wva / 10_000 / 1_000     # mld EUR
    d_assets = D_A * INV_21 * avg_sh_wva / 10_000 / 1_000        # mld EUR
    d_bel_obs = (BEL_22 - BEL_21) / 1_000_000                    # mld EUR
    residuo = d_bel_obs - d_bel_rate / 1000 if False else (BEL_22 - BEL_21) / 1_000 - d_bel_rate * 1000
    print(f"shift medio with_VA 2021->2022 : +{avg_sh_wva:.3f} (decimale) = {avg_sh_wva*10:.0f} bp... uso bps: {avg_sh_wva*10000 if False else ''}")
    print(f"dBEL solo-tasso [E-derived]    : {d_bel_rate:+.1f} mld EUR")
    print(f"dBEL osservato [O]             : {d_bel_obs:+.1f} mld EUR")
    print(f"residuo non-tasso              : {d_bel_obs - d_bel_rate:+.1f} mld EUR (runoff, nuovi affari, DPHB)")
    print(f"dAssets [E-derived]            : {d_assets:+.1f} mld EUR")
    print(f"contributo dinamico netto      : {d_assets + d_bel_rate:+.1f} mld EUR (era +1,41 con [E] +250bp)")

    print("\n== 4. Duration implicite dal VA (finding DPHB) ==")
    for date, tp in (("2021-12-31", TP_21), ("2022-12-31", TP_22)):
        d = VA_TP_IMPACT[date] / (tp * VA_BY_DATE(df, date) / 10_000)
        print(f"{date}: impatto VA->0 TP {VA_TP_IMPACT[date]:,} su TP {tp:,} -> D implicita {d:.2f}")


def VA_BY_DATE(df: pl.DataFrame, date: str) -> int:
    return int(df.filter(pl.col("ref_date") == date)["va_bps"][0])


if __name__ == "__main__":
    main()

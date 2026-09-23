#!/usr/bin/env python3
"""
06_panel_2019_2024.py — Analisi pluriennale del panel esteso [O] 2019-2024.

1. Serie TMTP in run-off (argomento prevedibilità per il motore dinamico)
2. Serie VA->0 su TP con anomalia 2021 isolata
3. Ratio V-shape 2022->2023 e decomposizione statico/dinamico per anno
4. Variazioni YoY di EOF, SCR e ratio con segno (stress detector)
"""
from __future__ import annotations

from pathlib import Path

import polars as pl

REPO = Path(__file__).resolve().parents[1]
PANEL = REPO / "data" / "interim" / "company_sfcr_2019_2020.csv"
PANEL_MAIN = REPO / "data" / "interim" / "company_sfcr_interim.csv"

YEARS = [2019, 2020, 2021, 2022, 2023, 2024]
TP = {2019: 132_764_862, 2020: 147_434_522, 2021: 151_694_417, 2022: 133_029_385, 2023: 145_741_821, 2024: 152_319_265}
TMTP = {2019: 1_908_091, 2020: 1_749_084, 2021: 1_590_076, 2022: 0, 2023: 0, 2024: 0}
EOF = {2019: 11_468_565, 2020: 11_193_573, 2021: 12_676_835, 2022: 12_804_895, 2023: 14_098_823, 2024: 13_920_129}
SCR = {2019: 3_675_204, 2020: 3_739_960, 2021: 4_441_175, 2022: 5_055_992, 2023: 4_591_654, 2024: 4_314_983}
RATIO = {2019: 312.00, 2020: 299.27, 2021: 285.40, 2022: 253.26, 2023: 307.05, 2024: 322.60}
VA_TP = {2019: 537_028, 2020: 669_737, 2021: 217_453, 2022: 565_931, 2023: 571_199, 2024: 572_475}
# SCR 2020 [E-derived] dal ratio dichiarato; tutto il resto [O] (SOURCES + addendum)
SCR[2020] = round(EOF[2020] / (RATIO[2020] / 100))  # ~3.739.960


def main() -> None:
    df = pl.DataFrame({
        "year": YEARS,
        "tp_mln": [TP[y] / 1e3 for y in YEARS],
        "tmtp_mln": [TMTP[y] / 1e3 for y in YEARS],
        "eof_mln": [EOF[y] / 1e3 for y in YEARS],
        "scr_mln": [SCR[y] / 1e3 for y in YEARS],
        "ratio_pct": [RATIO[y] for y in YEARS],
        "va_tp_mln": [VA_TP[y] / 1e3 for y in YEARS],
    }).with_columns(
        d_ratio=(pl.col("ratio_pct") - pl.col("ratio_pct").shift(1)).round(2),
        d_scr_mln=(pl.col("scr_mln") - pl.col("scr_mln").shift(1)).round(1),
        d_eof_mln=(pl.col("eof_mln") - pl.col("eof_mln").shift(1)).round(1),
    )
    print(df)

    print("\n== 1. TMTP run-off (25% annuo 2019-2021, poi azzerato) ==")
    for y in (2020, 2021, 2022):
        pct = (TMTP[y] / TMTP[y - 1] - 1) * 100 if TMTP[y - 1] else float("nan")
        print(f"  {y}: {TMTP[y]:,} ({pct:+.1f}%)")
    print("  -> decadimento programmato e prevedibile: catturabile da un motore dinamico, non da uno statico")

    print("\n== 2. VA->0 su TP: anomalia 2021 ==")
    mean_ex_2021 = sum(VA_TP[y] for y in YEARS if y != 2021) / 5
    print(f"  media 2020/2022-2024: {mean_ex_2021/1e3:.0f} mln vs 2021: {VA_TP[2021]/1e3:.0f} mln")
    print(f"  2021 = {-((VA_TP[2021]/mean_ex_2021)-1)*100:.0f}% sotto la media: anno base atipico (VA EIOPA 3 bps)")

    print("\n== 3. V-shape 2022->2023 ==")
    print(f"  ratio: {RATIO[2022]:.1f}% -> {RATIO[2023]:.1f}% (+{RATIO[2023]-RATIO[2022]:.1f}pp)")
    print(f"  driver: EOF +{(EOF[2023]-EOF[2022])/1e3:.0f} mln, SCR -{(SCR[2022]-SCR[2023])/1e3:.0f} mln")

    print("\n== 4. Stress detector (|d_ratio| > 10pp) ==")
    for i in range(1, len(YEARS)):
        dr = RATIO[YEARS[i]] - RATIO[YEARS[i - 1]]
        flag = " <<< STRESS" if abs(dr) > 10 else ""
        print(f"  {YEARS[i]}: d_ratio {dr:+.2f}pp (EOF {EOF[YEARS[i]]-EOF[YEARS[i-1]]:+,}, SCR {SCR[YEARS[i]]-SCR[YEARS[i-1]]:+,}){flag}")


if __name__ == "__main__":
    main()

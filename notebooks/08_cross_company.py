#!/usr/bin/env python3
"""
08_cross_company.py — Analisi campionaria inter-compagnia [O].

1. Matrice ratio per compagnia x anno (gap-filling esplicito: n.d. mostrato)
2. Stesso shock 2022, direzioni opposte: delta ratio 2021->2022 per compagnia
3. VA dichiarato vs curve EIOPA estratte (cross-check sistemico)
4. Eterogeneita' dei motori: MIP vs Standard Formula (volatilita' SCR a confronto)
"""
from __future__ import annotations

import polars as pl

# [O] panel inter-compagnia (EUR k); ratio O=dichiarato, E=derived
ROWS = [
    # company, engine, year, eof, scr, ratio, ratio_q, va_bps
    ("PV_GROUP", "SF", 2020, 11_193_573, 3_739_960, 299.27, "E", None),
    ("PV_GROUP", "SF", 2021, 12_676_835, 4_441_175, 285.40, "O", 3),
    ("PV_GROUP", "SF", 2022, 12_804_895, 5_055_992, 253.26, "O", 19),
    ("PV_GROUP", "SF", 2023, 14_098_823, 4_591_654, 307.05, "O", 20),
    ("PV_GROUP", "SF", 2024, 13_920_129, 4_314_983, 322.60, "O", 23),
    ("ARCA_VITA", "MIP", 2020, 701_837, 217_557, 323.00, "O", 7),
    ("ARCA_VITA", "MIP", 2021, 771_922, 264_833, 291.47, "E", 3),
    ("ARCA_VITA", "MIP", 2022, 788_825, 252_912, 311.96, "E", 19),
    ("ARCA_VITA", "MIP", 2023, 884_819, 378_305, 233.87, "E", 20),
    ("ARCA_VITA", "MIP", 2024, 956_528, 396_117, 241.00, "O", 23),
    ("ARCA_VITA", "MIP", 2025, 1_095_439, 430_793, 254.00, "O", 14),
    ("ISV_GROUP", "SF", 2022, 9_208_916, 4_536_557, 203.01, "E", None),
    ("ISV_GROUP", "SF", 2023, 9_761_000, 3_954_500, 246.86, "E", None),
    ("ISPA_GROUP", "SF", 2024, 9_373_700, 3_862_000, 242.72, "E", None),
    ("ISPA_GROUP", "SF", 2025, 10_898_521, 4_193_635, 259.91, "E", None),
]


def main() -> None:
    df = pl.DataFrame(
        [{"company": r[0], "engine": r[1], "year": r[2], "eof": r[3], "scr": r[4],
          "ratio": r[5], "ratio_q": r[6], "va_bps": r[7]} for r in ROWS]
    )

    print("== 1. Matrice ratio (n.d. = dato non disponibile, NON interpolato) ==")
    piv = df.pivot(on="company", index="year", values="ratio").sort("year")
    print(piv)

    print("\n== 2. Stesso shock 2022 (stessa curva +307bps, stesso VA 19bps), delta ratio 2021->2022 ==")
    for c in ("PV_GROUP", "ARCA_VITA"):
        r21 = df.filter((pl.col("company") == c) & (pl.col("year") == 2021))["ratio"][0]
        r22 = df.filter((pl.col("company") == c) & (pl.col("year") == 2022))["ratio"][0]
        d_eof = df.filter((pl.col("company") == c) & (pl.col("year") == 2022))["eof"][0] - \
                df.filter((pl.col("company") == c) & (pl.col("year") == 2021))["eof"][0]
        d_scr = df.filter((pl.col("company") == c) & (pl.col("year") == 2022))["scr"][0] - \
                df.filter((pl.col("company") == c) & (pl.col("year") == 2021))["scr"][0]
        print(f"  {c}: {r21:.1f}% -> {r22:.1f}% ({r22-r21:+.1f}pp) | dEOF {d_eof/1e3:+.0f} mln, dSCR {d_scr/1e3:+.0f} mln")
    print("  -> direzioni OPPOSTE sullo stesso shock di mercato: il motore statico sbaglia due volte")

    print("\n== 3. VA dichiarato vs curve EIOPA estratte (rfr_curves_eur_2021_2022.csv) ==")
    eiopa = {2021: 3, 2022: 19}
    for y in (2021, 2022):
        declared = df.filter((pl.col("company") == "ARCA_VITA") & (pl.col("year") == y))["va_bps"][0]
        pvg = df.filter((pl.col("company") == "PV_GROUP") & (pl.col("year") == y))["va_bps"][0]
        ok = declared == eiopa[y] == pvg
        print(f"  {y}: Arca {declared} bps, PVG {pvg} bps, curve EIOPA {eiopa[y]} bps -> {'COERENTE' if ok else 'MISMATCH'}")

    print("\n== 4. Volatilita' SCR per motore (std dei delta % YoY) ==")
    for c in ("PV_GROUP", "ARCA_VITA"):
        scrs = df.filter(pl.col("company") == c).sort("year")["scr"].to_list()
        deltas = [(b / a - 1) * 100 for a, b in zip(scrs, scrs[1:])]
        import statistics
        print(f"  {c}: delta% YoY {['%+.1f' % d for d in deltas]} -> std {statistics.stdev(deltas):.1f}pp")


if __name__ == "__main__":
    main()

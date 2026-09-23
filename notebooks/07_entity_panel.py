#!/usr/bin/env python3
"""
07_entity_panel.py — Analisi campionaria per entita' (PV solo, PA, Net) 2020-2024 [O].

1. Serie ratio per entita' e dispersione trasversale (std dei ratio per anno)
2. Decomposizione dei driver: delta EOF vs delta SCR per entita' (chi guida il ratio)
3. Volatilita' relativa: |delta SCR| / SCR medio per taglia (effetto taglia)
4. Regimi eterogenei: tassi (PV) vs vigilanza (PA add-on) vs taglia (Net)
"""
from __future__ import annotations

import polars as pl

# [O] da entity_panel_2019_2024.csv / SOURCES (EUR k); n.d. = None
RATIO = {  # (entity, year) -> ratio %
    ("PV_SOLO", 2020): 299.83, ("PV_SOLO", 2021): 288.0, ("PV_SOLO", 2022): 257.78,
    ("PV_SOLO", 2023): 310.65, ("PV_SOLO", 2024): 333.17,
    ("PA_SOLO", 2020): 311.31, ("PA_SOLO", 2021): 242.3, ("PA_SOLO", 2023): 234.58, ("PA_SOLO", 2024): 234.98,
    ("NET_SOLO", 2023): 235.34, ("NET_SOLO", 2024): 229.54,
    ("PV_GROUP", 2020): 299.27, ("PV_GROUP", 2021): 285.4, ("PV_GROUP", 2022): 253.26,
    ("PV_GROUP", 2023): 307.05, ("PV_GROUP", 2024): 322.6,
}
EOF = {
    ("PV_SOLO", 2022): 12_804_895, ("PV_SOLO", 2023): 14_079_290, ("PV_SOLO", 2024): 13_899_090,
    ("PA_SOLO", 2023): 371_389, ("PA_SOLO", 2024): 438_856,
    ("NET_SOLO", 2022): 33_217, ("NET_SOLO", 2023): 47_909, ("NET_SOLO", 2024): 60_172,
}
SCR = {
    ("PV_SOLO", 2022): 4_967_417, ("PV_SOLO", 2023): 4_532_196, ("PV_SOLO", 2024): 4_171_784,
    ("PA_SOLO", 2023): 158_321, ("PA_SOLO", 2024): 186_766,
    ("NET_SOLO", 2023): 20_357,
}


def main() -> None:
    df = pl.DataFrame(
        [{"entity": e, "year": y, "ratio": r} for (e, y), r in RATIO.items()]
    ).sort(["year", "entity"])

    print("== 1. Serie ratio per entita' ==")
    print(df.pivot(on="entity", index="year", values="ratio").sort("year"))

    print("\n== 2. Dispersione trasversale (std dei ratio per anno) ==")
    disp = df.group_by("year").agg(pl.col("ratio").std().alias("std_ratio"), pl.len().alias("n")).sort("year")
    print(disp)

    print("\n== 3. Driver del delta ratio 2023->2024 (EOF vs SCR, %) ==")
    for e in ("PV_SOLO", "PA_SOLO"):
        d_eof = (EOF[(e, 2024)] / EOF[(e, 2023)] - 1) * 100
        d_scr = (SCR[(e, 2024)] / SCR[(e, 2023)] - 1) * 100
        print(f"  {e}: dEOF {d_eof:+.1f}%, dSCR {d_scr:+.1f}% -> ratio {RATIO[(e,2023)]:.1f} -> {RATIO[(e,2024)]:.1f}")
    print("  NET_SOLO: dEOF +25.5% (SCR 2024 n.d.) -> ratio 235,3 -> 229,5")

    print("\n== 4. Effetto taglia: volatilita' relativa |dSCR|/SCR 2023->2024 ==")
    print("  PV solo: 8.0% | PA: 18.0% | Net: n.d. (SCR 2024 non estratto; dEOF +25,5%)")
    print("  -> al diminuire della taglia, la volatilita' relativa del requisito aumenta")


if __name__ == "__main__":
    main()

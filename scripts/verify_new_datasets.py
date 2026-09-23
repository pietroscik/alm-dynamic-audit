#!/usr/bin/env python3
"""verify_new_datasets.py — invarianti QA per i dataset aggiunti dopo 1eaf071.

Implementa l'Appendice A §A.4 (punti 2-4) per:
- data/processed/rfr_curves_eur_2023_2026.csv (20 nodi x 2 sheet x 4 date; va_bps = round((wv-nv)*1e4))
- data/processed/backtest_static_vs_dynamic_2021_2026.csv (P statico costante; 6 righe)
- data/interim/lapse_flows_pvg.csv e lapse_flows_pvg_ext.csv (tag/source_doc/source_section su [O])
Exit != 0 al primo fallimento. Nessun dato inventato: solo verifica.
"""
from __future__ import annotations
import csv
import sys
from collections import defaultdict
from pathlib import Path

FAIL: list[str] = []


def check(cond: bool, msg: str) -> None:
    if not cond:
        FAIL.append(msg)


def main() -> int:
    root = Path(__file__).resolve().parents[1]

    # --- curve 2023-2026 ---
    p = root / "data/processed/rfr_curves_eur_2023_2026.csv"
    check(p.exists(), f"missing {p}")
    if p.exists():
        by_date_sheet: dict[tuple[str, str], set[int]] = defaultdict(set)
        with p.open(newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                mat = int(row["maturity"])
                by_date_sheet[(row["date"], "no_va")].add(mat)
                by_date_sheet[(row["date"], "with_va")].add(mat)
                va = int(row["va_bps"])
                expected = round((float(row["rfr_with_va"]) - float(row["rfr_no_va"])) * 10000)
                check(abs(va - expected) <= 1, f"va_bps mismatch {row['date']} m{mat}: {va} vs {expected}")
                check(row.get("quality") == "verified", f"quality not verified: {row['date']} m{mat}")
        check(len(by_date_sheet) == 8, f"expected 8 (date,sheet) combos, got {len(by_date_sheet)}")
        for (date, sheet), mats in by_date_sheet.items():
            check(mats == set(range(1, 21)), f"{date}/{sheet}: maturities incomplete ({len(mats)})")

    # --- backtest ---
    p = root / "data/processed/backtest_static_vs_dynamic_2021_2026.csv"
    check(p.exists(), f"missing {p}")
    if p.exists():
        statics: set[float] = set()
        n = 0
        with p.open(newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                n += 1
                statics.add(float(row["p10_static_eur"]))
        check(n == 6, f"backtest rows {n} != 6")
        check(len(statics) == 1, f"P statico non costante: {statics}")

    # --- lapse CSV: tracciabilita' ---
    for rel in ("data/interim/lapse_flows_pvg.csv", "data/interim/lapse_flows_pvg_ext.csv"):
        p = root / rel
        check(p.exists(), f"missing {p}")
        if p.exists():
            with p.open(newline="", encoding="utf-8") as f:
                for row in csv.DictReader(f):
                    if row.get("tag", "").startswith("[O"):
                        check(bool(row.get("source_doc")), f"{rel}: [O] senza source_doc ({row.get('metric')})")
                        check(bool(row.get("source_section")), f"{rel}: [O] senza source_section ({row.get('metric')})")

    if FAIL:
        print("VERIFY NEW DATASETS: FAIL")
        for m in FAIL:
            print(" -", m)
        return 1
    print("VERIFY NEW DATASETS: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())

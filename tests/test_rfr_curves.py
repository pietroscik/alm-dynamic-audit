#!/usr/bin/env python3
"""test_rfr_curves.py — validità e cross-validation delle curve EIOPA RFR [O].

Cross-validation chiave: il VA EUR 31/12/2022 = 19 bps DEVE coincidere con il VA
dichiarato nell'SFCR PVG 2022 (Relazione Unica, D.2). La duration implicita 2021
dal VA (3 bps, impatto TP 217.453 su TP 151.694.417) deve essere ~4,78 — coerente
con D_L≈5,30 del notebook. Se questi test falliscono, il dato NON entra come [O].
"""
from __future__ import annotations

import csv
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
CURVES = REPO / "data" / "processed" / "rfr_curves_eur_2021_2022.csv"

DATES = {"2021-12-31", "2022-05-31", "2022-09-30", "2022-12-31"}
EXPECTED_VA = {"2021-12-31": 3, "2022-05-31": 14, "2022-09-30": 17, "2022-12-31": 19}

# [O] SFCR PVG: impatto VA->0 su TP (EUR k)
VA_TP_IMPACT_2021 = 217_453
TP_2021 = 151_694_417


def load():
    with open(CURVES, newline="") as f:
        return list(csv.DictReader(f))


def test_rows_complete_and_verified():
    rows = load()
    assert rows, "CSV curve vuoto"
    per = {}
    for r in rows:
        assert r["quality"] == "verified", f"riga non verified: {r}"
        per.setdefault((r["ref_date"], r["sheet"]), set()).add(int(r["maturity"]))
    for date in DATES:
        for sheet in ("no_VA", "with_VA"):
            assert per.get((date, sheet)) == set(range(1, 21)), f"nodi mancanti {date}/{sheet}"


def test_va_flat_and_matches_sfcr():
    for r in load():
        assert int(r["va_bps"]) == EXPECTED_VA[r["ref_date"]], f"VA non conforme: {r}"


def test_curves_monotonic_2021():
    """31/12/2021 la curva EUR è crescente fino al LLP (20) — sanity del parsing."""
    rates = {int(r["maturity"]): float(r["rate"]) for r in load()
             if r["ref_date"] == "2021-12-31" and r["sheet"] == "no_VA"}
    seq = [rates[m] for m in range(1, 21)]
    assert all(b >= a for a, b in zip(seq, seq[1:])), "curva 2021 non monotona: parsing sospetto"


def test_implied_duration_2021_from_va():
    d = VA_TP_IMPACT_2021 / (TP_2021 * EXPECTED_VA["2021-12-31"] / 10_000)
    assert 4.5 < d < 5.2, f"duration implicita 2021 anomala: {d:.2f}"

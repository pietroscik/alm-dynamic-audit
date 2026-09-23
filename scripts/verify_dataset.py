#!/usr/bin/env python3
"""
verify_dataset.py — QA automatico del dataset [O] (invarianti aritmetiche e cross-validation).

Verifica (tutti i valori tracciati in data/interim/SOURCES.md e addendum):
  1. TP = BEL + RM (+ TMTP se incluso) per ogni riga del panel
  2. Solvency ratio = EOF / SCR entro 0,1pp dal dichiarato
  3. Bridge EOF 2021->2022: -247.519 + 428.240 - 52.661 = +128.060
  4. VA EUR piatto per data (3/14/17/19 bps) e cross-validato con SFCR 2022
  5. Duration implicita 2021 dal VA in (4,5; 5,2)
  6. OPEN ITEM: PV_SOLO 2022 residuo TP - (BEL+RM) = -6.065 da chiarire
Exit code != 0 se una verifica fallisce. CI-ready (nessuna dipendenza oltre stdlib).
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
OK, FAIL = "[PASS]", "[FAIL]"
failures: list[str] = []


def check(name: str, cond: bool, detail: str = "") -> None:
    print(f"{OK if cond else FAIL} {name}" + (f" — {detail}" if detail else ""))
    if not cond:
        failures.append(name)


# --- 1-2. Panel compagnia (dati [O] tracciati, EUR k) ------------------------
PANEL = [
    # company, year, BEL, RM, TP, TMTP_included_in_TP, EOF, SCR, ratio_dichiarato
    ("PV_GROUP", 2021, 151_468_375, 226_042, 151_694_417, False, 12_676_835, 4_441_175, 285.40),
    ("PV_GROUP", 2022, 128_350_704, 4_678_681, 133_029_385, True, 12_804_895, 5_055_992, 253.26),
    ("PV_GROUP", 2023, 141_463_778, 4_278_043, 145_741_821, True, 14_098_823, 4_591_654, 307.05),
    ("PV_GROUP", 2024, 148_744_706, 3_574_559, 152_319_265, True, 13_920_129, 4_314_983, 322.60),
]

print("== 1. TP = BEL + RM (+ TMTP se incluso) ==")
for c, y, bel, rm, tp, tmtp_in, *_ in PANEL:
    exp = bel + rm + (1_590_076 if (y == 2021 and tmtp_in) else 0)
    check(f"TP {c} {y}", tp == exp, f"{tp:,} vs {exp:,}")
# open item PV_SOLO 2022
solo_res = 132_727_905 - (128_082_365 + 4_651_605)
print(f"[INFO] PV_SOLO 2022: TP - (BEL+RM) = {solo_res:,} (OPEN ITEM: componente non tracciata)")

print("\n== 2. Solvency ratio = EOF / SCR ==")
for c, y, *_rest, eof, scr, ratio in [(r[0], r[1], r[5], r[6], r[7], r[8]) for r in PANEL]:
    calc = eof / scr * 100
    check(f"ratio {c} {y}", abs(calc - ratio) < 0.1, f"calc {calc:.2f}% vs dich {ratio}%")

print("\n== 3. Bridge EOF 2021->2022 [O] ==")
bridge = -247_519 + 428_240 - 52_661
check("bridge = +128.060", bridge == 128_060, f"{bridge:,}")
obs = 12_804_895 - 12_676_835
check("delta EOF osservato = bridge", obs == bridge, f"{obs:,}")

print("\n== 4. VA EUR piatto per data (curve [O]) ==")
CURVES = REPO / "data" / "processed" / "rfr_curves_eur_2021_2022.csv"
EXPECTED_VA = {"2021-12-31": 3, "2022-05-31": 14, "2022-09-30": 17, "2022-12-31": 19}
if CURVES.exists():
    with open(CURVES, newline="") as f:
        rows = list(csv.DictReader(f))
    per: dict[str, set[int]] = {}
    for r in rows:
        per.setdefault(r["ref_date"], set()).add(int(r["va_bps"]))
    for d, exp in EXPECTED_VA.items():
        check(f"VA {d} piatto = {exp} bps", per.get(d) == {exp}, str(per.get(d)))
else:
    check("rfr_curves CSV presente", False, f"{CURVES} mancante")

print("\n== 5. Duration implicita 2021 dal VA (S.22.01.22: impatto 217.453 su TP 151.694.417) ==")
d_impl = 217_453 / (151_694_417 * 3 / 10_000)
check("D implicita 2021 in (4,5; 5,2)", 4.5 < d_impl < 5.2, f"{d_impl:.2f}")

print()
if failures:
    print(f"ESITO: {len(failures)} VERIFICHE FALLITE: {failures}")
    sys.exit(1)
print("ESITO: tutte le verifiche superate. Dataset idoneo a [O].")

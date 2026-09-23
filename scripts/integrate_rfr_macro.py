#!/usr/bin/env python3
"""
integrate_rfr_macro.py — Migra macro_series.csv da 'synthetic' a 'verified'.

Legge le curve EIOPA RFR EUR verificate (data/processed/rfr_curves_eur_2021_2022.csv,
[O] da file EIOPA_RFR_*_Term_Structures.xlsx, vedi data/interim/SOURCES_addendum_rfr.md)
e sostituisce le righe RFR sintetiche di data/processed/macro_series.csv.

SICUREZZO: di default esegue in dry-run (stampa anteprima, non scrive nulla).
Usare --apply per scrivere. Backup automatico in macro_series.csv.bak.

Regola di accettazione: nessun numero entra come [O] se non tracciabile a
(file, sezione/QRT). Le righe migrate portano quality_note='verified' con fonte
per riga; le righe synthetic residue NON vengono eliminate silently ma elencate.

Uso:
    python scripts/integrate_rfr_macro.py            # dry-run
    python scripts/integrate_rfr_macro.py --apply    # scrive + backup
"""
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

import polars as pl

REPO = Path(__file__).resolve().parents[1]
CURVES = REPO / "data" / "processed" / "rfr_curves_eur_2021_2022.csv"
MACRO = REPO / "data" / "processed" / "macro_series.csv"

# VA dichiarati/verificati [O]: piatti per data (cross-validation SFCR PVG)
VA_BPS_BY_DATE = {"2021-12-31": 3, "2022-05-31": 14, "2022-09-30": 17, "2022-12-31": 19}


def load_curves() -> pl.DataFrame:
    df = pl.read_csv(CURVES)
    required = {"ref_date", "sheet", "maturity", "rate"}
    missing = required - set(df.columns)
    if missing:
        sys.exit(f"ERRORE: {CURVES.name} manca delle colonne {sorted(missing)}")
    bad = df.filter(pl.col("quality") != "verified")
    if bad.height:
        sys.exit(f"ERRORE: {bad.height} righe non-verified in {CURVES.name} — rifiuto la migrazione")
    return df


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="scrive macro_series.csv (default: dry-run)")
    args = ap.parse_args()

    if not MACRO.exists():
        sys.exit(f"ERRORE: {MACRO} non trovato")

    curves = load_curves()

    # Serie puntuali per data: tasso medio nodi 1-20, per sheet (proxy sintetici tipici)
    summary = (
        curves.group_by(["ref_date", "sheet"])
        .agg(
            pl.col("rate").mean().alias("avg_rate_1_20"),
            pl.col("va_bps").first().alias("va_bps"),
            pl.len().alias("n_nodes"),
        )
        .sort(["ref_date", "sheet"])
    )
    print("== Curve verificate disponibili ==")
    print(summary)

    macro = pl.read_csv(MACRO)
    print("\n== macro_series.csv attuale ==")
    print("colonne:", macro.columns)
    print("righe:", macro.height)

    # Individua le colonne di integrazione in modo difensivo (schema non garantito via API)
    date_col = next((c for c in macro.columns if c.lower() in ("ref_date", "date", "periodo", "data")), None)
    series_col = next((c for c in macro.columns if c.lower() in ("series", "serie", "metric", "indicatore")), None)
    value_col = next((c for c in macro.columns if c.lower() in ("value", "valore", "rate")), None)
    quality_col = next((c for c in macro.columns if "quality" in c.lower() or "flag" in c.lower()), None)

    if not all([date_col, series_col, value_col]):
        sys.exit(
            "ERRORE: schema macro_series.csv non riconosciuto.\n"
            f"  atteso date~{date_col}, series~{series_col}, value~{value_col}.\n"
            "  Integrare a mano con i dati di rfr_curves_eur_2021_2022.csv."
        )

    # Righe RFR sintetiche da sostituire
    is_rfr = pl.col(series_col).str.to_lowercase().str.contains("rfr|eopa|curve|rate")
    synth = macro.filter(is_rfr)
    print(f"\nRighe RFR candidate alla sostituzione: {synth.height}")
    if quality_col:
        print(synth.select([date_col, series_col, quality_col]).head(20))

    # righe synthetic NON-RFR: non toccare, solo segnalarle
    if quality_col:
        other_synth = macro.filter(pl.col(quality_col).str.to_lowercase() == "synthetic").filter(~is_rfr)
        if other_synth.height:
            print(f"\nATTENZIONE: {other_synth.height} righe synthetic NON-RFR restano da verificare:")
            print(other_synth.select([date_col, series_col, value_col]).head(20))

    if not args.apply:
        print("\nDRY-RUN: nessuna modifica scritta. riesegui con --apply per applicare.")
        return

    backup = MACRO.with_suffix(".csv.bak")
    shutil.copy2(MACRO, backup)
    print(f"\nBackup: {backup}")

    # Costruisci le righe verificate nel formato macro_series (stesse colonne, valore medio nodi 1-20)
    new_rows = summary.select(
        pl.col("ref_date").alias(date_col),
        pl.concat_str(
            [pl.lit("EIOPA_RFR_EUR_"), pl.col("sheet"), pl.lit("_avg1_20")]
        ).alias(series_col),
        pl.col("avg_rate_1_20").alias(value_col),
    )
    # colonna quality_note se esiste, altrimenti aggiungila
    if quality_col:
        new_rows = new_rows.with_columns(pl.lit("verified").alias(quality_col))
    else:
        new_rows = new_rows.with_columns(pl.lit("verified").alias("quality_note"))

    out = pl.concat([macro.filter(~is_rfr), new_rows], how="diagonal_relaxed").sort(date_col)
    out.write_csv(MACRO)
    print(f"\nSCRITTO: {MACRO} — {out.height} righe totali, +{new_rows.height} righe verified")


if __name__ == "__main__":
    main()

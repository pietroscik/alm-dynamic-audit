"""Parser dei file Excel EIOPA RFR (Layer 1 raw -> Layer 2 interim).

Il file Excel ufficiale EIOPA (es. EIOPA_RFR_2022-12-30_Term_Structures.xlsx)
contiene un foglio per valuta: "EUR" con e senza Volatility Adjustment.
Questo estrae i nodi richiesti per entrambe le curve e li scrive in un
CSV interim normalizzato (decimale, long format).

USO:
    from src.eiopa_loader import parse_eiopa_workbook
    df = parse_eiopa_workbook("data/raw/EIOPA_RFR_2022-12-30.xlsx")
    df.write_csv("data/interim/eiopa_rfr_2022-12-30.csv")

Non fa ipotesi sul nome esatto del foglio: li scorre tutti e cerca
la colonna delle scadenze. I tassi EIOPA sono in percentuale:
la conversione a decimale avviene QUI, una volta sola.
Attenzione date: EIOPA calcola sull'ultimo giorno lavorativo
(es. dicembre 2022 -> riferimento 2022-12-30, non 31).
"""

from __future__ import annotations

from pathlib import Path

import polars as pl

WANTED_TENORS = {
    "1", "2", "3", "5", "7", "10", "15", "20",  # etichette EIOPA (anni)
}


def parse_eiopa_workbook(path: str | Path) -> pl.DataFrame:
    """Estrae i nodi EUR (con e senza VA) da un file EIOPA.

    Ritorna un DataFrame interim:
        ref_date, currency, tenor_years, rate_no_va, rate_with_va
    con i tassi gia' in decimale.
    """
    path = Path(path)
    if not path.exists():
        raise ValueError(f"File non trovato: {path}")

    # la ref date e' nel nome file: EIOPA_RFR_YYYY-MM-DD_...
    ref_date = None
    for part in path.stem.split("_"):
        if len(part) == 10 and part[4] == "-" and part[7] == "-":
            ref_date = part
            break
    if ref_date is None:
        raise ValueError(
            f"Data di riferimento non trovata nel nome file {path.name}: "
            f"usare la convenzione EIOPA_RFR_YYYY-MM-DD_*.xlsx"
        )

    rows: list[dict] = []
    xls = pl.read_excel(source=str(path), sheet_id=0,
                        infer_schema_length=0)  # tutto come stringa

    for sheet_name in xls.keys():
        df = pl.read_excel(source=str(path), sheet_name=sheet_name,
                           infer_schema_length=0)
        cols = [c for c in df.columns]
        # individua la colonna delle scadenze (di solito "Term" o simile)
        term_col = None
        for c in cols:
            if "term" in str(c).lower() or "maturity" in str(c).lower():
                term_col = c
                break
        if term_col is None:
            continue

        # individua le colonne dei tassi EUR con/senza VA
        rate_cols = {}
        for c in cols:
            cl = str(c).lower()
            if c == term_col:
                continue
            if "eur" in cl or "without" in cl or "va" in cl or "coupon" in cl:
                rate_cols[c] = cl

        if not rate_cols:
            continue

        for row in df.iter_rows(named=True):
            tenor = str(row[term_col]).strip()
            # EIOPA etichetta i nodi in anni interi o "10Y" a seconda
            # della versione: normalizziamo
            tenor_clean = tenor.replace("Y", "").replace("y", "").strip()
            if tenor_clean not in WANTED_TENORS:
                continue
            rec = {
                "ref_date": ref_date,
                "currency": "EUR",
                "tenor_years": int(tenor_clean),
                "sheet": sheet_name,
            }
            for c, _ in rate_cols.items():
                val = row[c]
                try:
                    v = float(str(val).replace(",", "."))
                except (TypeError, ValueError):
                    v = None
                rec[str(c)] = v
            rows.append(rec)

    if not rows:
        raise ValueError(
            f"Nessun nodo estratto da {path.name}: verificare la struttura "
            f"del foglio (colonne Term/EUR). I nomi dei fogli trovati erano: "
            f"{list(xls.keys())}"
        )

    interim = pl.DataFrame(rows)

    # conversione percentuale -> decimale, colonna per colonna tasso
    rate_cols = [c for c in interim.columns
                 if c not in ("ref_date", "currency", "tenor_years", "sheet")]
    for c in rate_cols:
        interim = interim.with_columns((pl.col(c) / 100.0).alias(c))

    # assegnazione con/senza VA in base ai nomi colonna del file:
    # la colonna con "VA"/"volatility" e' quella con aggiustamento
    no_va = [c for c in rate_cols
             if "no_va" in c.lower() or "without" in c.lower()]
    with_va = [c for c in rate_cols if c not in no_va]

    out = interim.select(
        ["ref_date", "currency", "tenor_years"]
        + ([no_va[0]] if no_va else [])
        + ([with_va[0]] if with_va else [])
    )
    final_cols = ["ref_date", "currency", "tenor_years"]
    rename = {}
    if no_va:
        rename[no_va[0]] = "rate_no_va"
        final_cols.append("rate_no_va")
    if with_va:
        rename[with_va[0]] = "rate_with_va"
        final_cols.append("rate_with_va")
    out = out.rename(rename).select(final_cols).sort("tenor_years")

    return out


def interim_to_macro(interim: pl.DataFrame) -> pl.DataFrame:
    """Converte l'interim EIOPA nel formato long di macro_series.

    Genera due serie per nodo: eiopa_rf_<t>y (senza VA, usata dai motori)
    ed eiopa_rf_<t>y_va (con VA, per confronto/analisi).
    """
    rows = []
    for row in interim.iter_rows(named=True):
        t = row["tenor_years"]
        if row.get("rate_no_va") is not None:
            rows.append((row["ref_date"], "EA", f"eiopa_rf_{t}y",
                         row["rate_no_va"], "EIOPA", "O"))
        if row.get("rate_with_va") is not None:
            rows.append((row["ref_date"], "EA", f"eiopa_rf_{t}y_va",
                         row["rate_with_va"], "EIOPA", "O"))
    return pl.DataFrame(
        rows,
        schema={"obs_date": pl.Utf8, "country": pl.Utf8,
                "series_name": pl.Utf8, "value": pl.Float64,
                "source": pl.Utf8, "obs_flag": pl.Utf8},
        orient="row",
    )

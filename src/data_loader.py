"""Layer di caricamento dati (Layer 3: processed).

Responsabilita' SOLE di questo modulo:
  - lettura CSV/Parquet,
  - uniformazione dei nomi colonna,
  - cast di date e float,
  - merge delle fonti.

Nessun controllo di qualita' qui: quelli vivono in data_quality.py.
Nessuna logica di modellazione qui.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import polars as pl

# Mappatura nome colonna sorgente -> nome colonna canonico.
# La chiave e' case-insensitive: normalizziamo tutto in snake_case.
CANONICAL_COLUMNS = {
    "companyid": "company_id",
    "companyname": "company_name",
    "reportdate": "report_date",
    "date": "report_date",  # fallback comune nei CSV macro
    "bel": "bel",
    "belreported": "bel",
    "ownfunds": "own_funds",
    "ownfundsreported": "own_funds",
    "scr": "scr",
    "scrreported": "scr",
    "solvencyratio": "solvency_ratio",
    "btpshare": "btp_share",
    "assetduration": "asset_duration",
    "liabilityduration": "liability_duration",
    "liabduration": "liability_duration",
    "cashbuffer": "cash_buffer",
    "sourcedoc": "source_doc",
    "sourcepage": "source_page",
    "qualityflag": "quality_flag",
    # macro_series
    "obsdate": "obs_date",
    "country": "country",
    "seriesname": "series_name",
    "value": "value",
    "source": "source",
    "obsflag": "obs_flag",
    # stress_scenarios
    "scenarioid": "scenario_id",
    "scenariodate": "scenario_date",
    "deltarfbps": "delta_rf_bps",
    "spreadbtpbps": "spread_btp_bps",
    "inflationyoy": "inflation_yoy",
    "lapsegamma": "lapse_gamma",
    "label": "label",
}

EXPECTED_COLUMNS = {
    "company_sfcr": [
        "company_id", "company_name", "report_date", "bel", "own_funds",
        "scr", "solvency_ratio", "btp_share", "asset_duration",
        "liability_duration", "cash_buffer", "source_doc", "source_page",
        "quality_flag",
    ],
    "macro_series": [
        "obs_date", "country", "series_name", "value", "source", "obs_flag",
    ],
    "stress_scenarios": [
        "scenario_id", "scenario_date", "delta_rf_bps", "spread_btp_bps",
        "inflation_yoy", "lapse_gamma", "label",
    ],
}

DATE_COLUMNS = {"report_date", "obs_date", "scenario_date"}
FLOAT_COLUMNS = {
    "bel", "own_funds", "scr", "solvency_ratio", "btp_share",
    "asset_duration", "liability_duration", "cash_buffer",
    "value", "delta_rf_bps", "spread_btp_bps", "inflation_yoy", "lapse_gamma",
}


def _normalize(name: str) -> str:
    return name.strip().lower().replace(" ", "_")


def load_table(path: str | Path, table_name: str) -> pl.DataFrame:
    """Carica una tabella processed, normalizza colonne e casta i tipi.

    Solleva ValueError se il file non esiste o se mancano colonne attese.
    """
    path = Path(path)
    if not path.exists():
        raise ValueError(f"File non trovato: {path}")

    if path.suffix == ".parquet":
        df = pl.read_parquet(path)
    else:
        df = pl.read_csv(path, try_parse_dates=True)

    # 1) normalizzazione nomi
    rename_map = {}
    for col in df.columns:
        norm = _normalize(col)
        canonical = CANONICAL_COLUMNS.get(norm, norm)
        rename_map[col] = canonical
    df = df.rename(rename_map)

    # 2) colonne obbligatorie
    required = EXPECTED_COLUMNS.get(table_name)
    if required is None:
        raise ValueError(f"Tabella sconosciuta: {table_name}")
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(
            f"[{table_name}] colonne mancanti in {path.name}: {missing}"
        )

    # 3) cast tipi
    for col in DATE_COLUMNS & set(df.columns):
        df = df.with_columns(pl.col(col).str.to_date(strict=False)
                             if df.schema[col] == pl.Utf8 else pl.col(col))
    for col in FLOAT_COLUMNS & set(df.columns):
        if df.schema[col] not in (pl.Float64,):
            df = df.with_columns(pl.col(col).cast(pl.Float64, strict=False))

    # 4) stringhe null-safe
    for col in ("company_id", "scenario_id", "series_name", "country",
                "side", "label"):
        if col in df.columns:
            df = df.with_columns(pl.col(col).cast(pl.Utf8).str.strip_chars())

    return df


def load_all(processed_dir: str | Path) -> dict[str, pl.DataFrame]:
    """Carica le tre tabelle base del MVP dal layer processed.

    I file mancanti producono un DataFrame vuoto, non un errore:
    la pipeline e' pensata per crescere per incrementi.
    """
    processed_dir = Path(processed_dir)
    tables: dict[str, pl.DataFrame] = {}
    files = {
        "company_sfcr": processed_dir / "company_sfcr.parquet",
        "macro_series": processed_dir / "macro_series.parquet",
        "stress_scenarios": processed_dir / "stress_scenarios.parquet",
    }
    for name, path in files.items():
        if path.exists():
            tables[name] = load_table(path, name)
        else:
            csv_fallback = path.with_suffix(".csv")
            if csv_fallback.exists():
                tables[name] = load_table(csv_fallback, name)
            else:
                tables[name] = pl.DataFrame()
    return tables


def join_scenario_with_company(
    company: pl.DataFrame, scenarios: pl.DataFrame
) -> pl.DataFrame:
    """Cross join compagnia x scenario (input ai motori statico/dinamico)."""
    return company.join(scenarios, how="cross")

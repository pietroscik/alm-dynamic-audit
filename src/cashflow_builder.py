"""Costruzione dei cash flow sintetici (ponte SFCR aggregato -> motore ALM).

Disclaimers metodologici (da modelspec.md):
  - NON replica il portafoglio reale: approssima il profilo temporale dei
    flussi compatibile con le metriche pubbliche osservabili (BEL,
    duration, composizione attivo).
  - Tutti gli output sono classificati [E] Estimated.

Metodo: profilo a "cumulata lineare" parametrizzato da un esponente di
concentrazione. Data una duration target D e un orizzonte T, si sceglie
il profilo w_t(t/T)^k il cui PV-duration eguaglia D; il flusso atteso
per nodo e' normalizzato perche' il PV dei flussi al tasso base eguagli
il valore in bilancio (BEL per il passivo, A per l'attivo).
"""

from __future__ import annotations

from datetime import date
from typing import Optional

import numpy as np
import polars as pl

from src.metrics import present_value, macaulay_duration


def _bucket_years(tenor: int) -> np.ndarray:
    return np.arange(1, tenor + 1, dtype=float)


def _fit_profile_exponent(
    tenor: int, target_duration: float, rate: float
) -> float:
    """Trova k tale che la duration del profilo w_t proporzionale a (t/T)^k
    sia circa il target.

    k crescente => flussi piu' back-loaded => duration maggiore.
    """
    t = _bucket_years(tenor)
    target = float(np.clip(target_duration, 0.1, tenor - 0.05))
    lo, hi = 0.0, 50.0
    for _ in range(80):  # bisezione: robusta e sufficiente
        k = 0.5 * (lo + hi)
        w = t**k
        pv = (w / (1 + rate) ** t).sum()
        dur = (t * w / (1 + rate) ** t).sum() / pv
        if dur < target:
            lo = k
        else:
            hi = k
    return 0.5 * (lo + hi)


def build_liability_cashflows(
    bel: float,
    liability_duration: float,
    tenor: int = 10,
    base_rate: float = 0.02,
    company_id: str = "C01",
    report_date: date = date(2022, 12, 31),
) -> pl.DataFrame:
    """Flussi passivi sintetici con PV = BEL e duration = circa target.

    Ritorna un DataFrame conforme a synthetic_cashflows.
    """
    t = _bucket_years(tenor)
    k = _fit_profile_exponent(tenor, liability_duration, base_rate)
    w = t**k
    pv_w = (w / (1 + base_rate) ** t).sum()
    scale = bel / pv_w
    cf = scale * w
    return pl.DataFrame({
        "company_id": [company_id] * tenor,
        "report_date": [report_date] * tenor,
        "side": ["liability"] * tenor,
        "bucket_year": t.astype(int),
        "cashflow": cf,
        "discount_curve": ["rf"] * tenor,
        "ode_flag": ["E"] * tenor,
    })


def build_asset_cashflows(
    total_assets: float,
    asset_duration: float,
    btp_share: float = 0.3,
    tenor: int = 10,
    base_rate: float = 0.02,
    company_id: str = "C01",
    report_date: date = date(2022, 12, 31),
) -> pl.DataFrame:
    """Flussi attivi sintetici, split sovrano / non-sovrano.

    La quota sovrana (btp_share) sconta su curva rf + spread,
    la quota restante su rf. PV totale = total_assets.
    """
    t = _bucket_years(tenor)
    k = _fit_profile_exponent(tenor, asset_duration, base_rate)
    w = t**k
    pv_w = (w / (1 + base_rate) ** t).sum()
    scale = total_assets / pv_w
    cf = scale * w

    rows = []
    for ti, cfi in zip(t.astype(int), cf):
        sovr = cfi * btp_share
        rest = cfi - sovr
        rows.append((company_id, report_date, "asset", ti, sovr,
                     "rf_plus_spread", "E"))
        rows.append((company_id, report_date, "asset", ti, rest, "rf", "E"))
    return pl.DataFrame(
        rows,
        schema={"company_id": pl.Utf8, "report_date": pl.Date, "side": pl.Utf8,
                "bucket_year": pl.Int64, "cashflow": pl.Float64,
                "discount_curve": pl.Utf8, "ode_flag": pl.Utf8},
        orient="row",
    )


def reshape_with_lapse(
    cf_liab: pl.DataFrame,
    lapse_rate: float,
    base_lapse: float = 0.05,
) -> pl.DataFrame:
    """Rimodella i flussi passivi per un tasso di riscatto osservato.

    La quota extra di riscatto (lapse_rate - base_lapse) anticipa
    pro-quota i flussi futuri agli anni precedenti (front-loading),
    conservando il valore totale nominale.

    Proprieta': se lapse_rate == base_lapse, i flussi sono invariati.
    """
    if lapse_rate <= base_lapse:
        return cf_liab

    extra = float(np.clip(lapse_rate - base_lapse, 0.0, 0.95))
    df = cf_liab.sort("bucket_year").with_columns(
        pl.col("cashflow").alias("cf_base")
    )
    cf = df["cf_base"].to_numpy().copy()

    for i in range(len(cf)):
        # quota anticipata dal nodo i+1 verso i (anno t -> t-1)
        moved = cf[i] * extra
        cf[i] -= moved
        if i == 0:
            cf[i] += moved  # anno 1: resta sul posto
        else:
            cf[i - 1] += moved

    return df.with_columns(
        pl.Series("cashflow", cf).alias("cashflow")
    ).drop("cf_base")


def total_assets_from_sfcr(row: dict) -> float:
    """Stima degli attivi totali: BEL + Own Funds (identita' di bilancio)."""
    return float(row["bel"]) + float(row["own_funds"])

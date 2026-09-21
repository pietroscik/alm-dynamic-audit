"""Funzioni finanziarie pure (numpy in, float/numpy out).

Nessun I/O, nessuna logica di scenario: solo matematica riutilizzabile
da static_engine, dynamic_engine e liquidity_engine.
"""

from __future__ import annotations

import numpy as np


def present_value(
    cashflows: np.ndarray, rates: np.ndarray | float
) -> float:
    """PV con scontamento composto annuo nodo per nodo.

    rates puo' essere scalare (curva piatta) o vettore lungo quanto
    i cashflows. rates e' il tasso per nodo (gia' eventuale spread).
    """
    cf = np.asarray(cashflows, dtype=float)
    t = np.arange(1, cf.size + 1)
    r = np.broadcast_to(np.asarray(rates, dtype=float), cf.shape)
    return float(np.sum(cf / (1.0 + r) ** t))


def macaulay_duration(
    cashflows: np.ndarray, rate: float
) -> float:
    cf = np.asarray(cashflows, dtype=float)
    t = np.arange(1, cf.size + 1)
    disc = (1.0 + rate) ** (-t)
    pv = float(np.sum(cf * disc))
    if pv <= 0:
        return 0.0
    return float(np.sum(t * cf * disc) / pv)


def modified_duration(
    cashflows: np.ndarray, rate: float
) -> float:
    return macaulay_duration(cashflows, rate) / (1.0 + rate)


def convexity(cashflows: np.ndarray, rate: float) -> float:
    cf = np.asarray(cashflows, dtype=float)
    t = np.arange(1, cf.size + 1)
    pv = float(np.sum(cf / (1.0 + rate) ** t))
    if pv <= 0:
        return 0.0
    num = float(np.sum(cf * t * (t + 1) / (1.0 + rate) ** (t + 2)))
    return num / pv


def duration_gap(asset_dur: float, liab_dur: float) -> float:
    return asset_dur - liab_dur


def parallel_shift(curve: np.ndarray, delta_bps: float) -> np.ndarray:
    """Shift parallelo in bps su una curva di tassi (decimali)."""
    return np.asarray(curve, dtype=float) + delta_bps / 10_000.0


def spread_sensitivity(
    cashflows: np.ndarray, curve: np.ndarray, spread_bps: float,
    weights: np.ndarray | None = None,
) -> float:
    """Differenza di PV tra curva con e senza spread.

    weights: quota di ogni nodo esposta allo spread (default tutti 1).
    """
    w = (np.ones(len(cashflows)) if weights is None
         else np.asarray(weights, dtype=float))
    pv_no = present_value(cashflows, curve)
    pv_yes = present_value(cashflows * w, np.asarray(curve) + spread_bps / 10_000.0)
    return pv_no - pv_yes


def liquidity_ratio(
    cf_in: float, cf_out: float, buffer: float
) -> float:
    """Copertura del fabbisogno di cassa dell'anno 1 (>=1 = coperto)."""
    need = cf_out - cf_in
    if need <= 0:
        return float("inf")
    return (cf_in + buffer) / need

"""Motore statico (benchmark lineare ortodosso).

Formule (modelspec.md, sezione 4):
    A_stat    = A_0  * (1 - D_mod^A * dr_par)
    BEL_stat  = BEL_0 * (1 - D_mod^L * dr_par)
    OF_stat   = A_stat - BEL_stat

Input: cash flow baseline + shock parallelo. Nessun comportamento
endogeno, nessuno spread, nessun costo di liquidita': per costruzione
e' il benchmark "cieco" rispetto a quelle non linearita'.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from src.metrics import modified_duration, convexity


@dataclass(frozen=True)
class StaticEngineInput:
    cf_asset: np.ndarray        # flussi attivi baseline
    cf_liab: np.ndarray         # flussi passivi baseline
    base_rate: float = 0.02     # tasso base per duration/convexity
    delta_rf_bps: float = 0.0   # shift parallelo equivalente dr_par


@dataclass(frozen=True)
class StaticEngineOutput:
    a_0: float
    bel_0: float
    a_stat: float
    bel_stat: float
    of_stat: float
    dur_mod_asset: float
    dur_mod_liab: float
    convexity_asset: float
    convexity_liab: float


def run_static_engine(inp: StaticEngineInput) -> StaticEngineOutput:
    dr = inp.delta_rf_bps / 10_000.0
    r = inp.base_rate

    dur_a = modified_duration(inp.cf_asset, r)
    dur_l = modified_duration(inp.cf_liab, r)
    conv_a = convexity(inp.cf_asset, r)
    conv_l = convexity(inp.cf_liab, r)

    # valori base (curva piatta al tasso base)
    a_0 = float(np.sum(
        inp.cf_asset / (1 + r) ** np.arange(1, len(inp.cf_asset) + 1)))
    bel_0 = float(np.sum(
        inp.cf_liab / (1 + r) ** np.arange(1, len(inp.cf_liab) + 1)))

    # approssimazione di primo ordine (benchmark lineare), con termine
    # di convessita' opzionale: manteniamo PRIMO ORDINE per fedelta' al
    # benchmark "lineare ortodosso" usato nel confronto.
    a_stat = a_0 * (1 - dur_a * dr)
    bel_stat = bel_0 * (1 - dur_l * dr)
    of_stat = a_stat - bel_stat

    return StaticEngineOutput(
        a_0=a_0, bel_0=bel_0,
        a_stat=a_stat, bel_stat=bel_stat, of_stat=of_stat,
        dur_mod_asset=dur_a, dur_mod_liab=dur_l,
        convexity_asset=conv_a, convexity_liab=conv_l,
    )

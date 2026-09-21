"""Motore dinamico: mark-to-market nodo per nodo con lapse endogeno.

Formule (modelspec.md, sezioni 2-3-5):
    L_t = min(L_max, L_base + gamma * max(0, r_mkt - r_port - c_fric))
    A_dyn    = somma CF_t^A / (1 + r_t + s_t)^t  (quota sovrana con spread)
    BEL_dyn  = somma CF~_t^L / (1 + r_t)^t        (flussi rimodellati dal lapse)
    OF_dyn   = A_dyn - BEL_dyn - C_liq            (C_liq da liquidity_engine)

Proprieta' di coerenza (test):
  - gamma=0 e s=0 => converge sul motore statico senza shift,
  - dr>0 => valore attivo lungo scende,
  - lapse maggiore => liability duration dinamica strettamente minore.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import polars as pl

from src.cashflow_builder import reshape_with_lapse
from src.metrics import macaulay_duration


@dataclass(frozen=True)
class DynamicEngineInput:
    cf_asset: np.ndarray            # flussi attivi baseline (mix curve)
    cf_liab: np.ndarray             # flussi passivi baseline
    curve_rf: np.ndarray            # curva EIOPA stressata (decimale, per nodo)
    spread_btp: float = 0.0         # spread in decimale sugli attivi sovrani
    sovereign_weight: np.ndarray | None = None  # quota per nodo esposta allo spread
    gamma: float = 0.0              # sensibilita' riscatti
    r_mkt: float = 0.04             # rendimento alternativo percepito (BTP breve)
    r_port: float = 0.01            # rendimento retrocesso dal portafoglio
    c_fric: float = 0.01            # frizione / penale di riscatto
    l_base: float = 0.05
    l_max: float = 0.40
    base_rate: float = 0.02         # per duration baseline


@dataclass(frozen=True)
class DynamicEngineOutput:
    lapse_rate: float
    a_dyn: float
    bel_dyn: float
    of_pre_liq: float               # OF dinamico prima dei costi di liquidazione
    liab_duration_dyn: float
    liab_duration_base: float
    cf_liab_reshaped: np.ndarray


def calculate_lapse_rate(
    base_lapse: float, mkt_rate: float, port_rate: float,
    gamma: float, c_fric: float = 0.01, l_max: float = 0.40,
) -> float:
    """L_t = min(L_max, L_base + gamma * max(0, r_mkt - r_port - c_fric))."""
    incentive = max(0.0, mkt_rate - port_rate - c_fric)
    return float(min(l_max, base_lapse + gamma * incentive))


def run_dynamic_engine(inp: DynamicEngineInput) -> DynamicEngineOutput:
    # 1) lapse endogeno
    lapse = calculate_lapse_rate(
        inp.l_base, inp.r_mkt, inp.r_port, inp.gamma,
        inp.c_fric, inp.l_max,
    )

    # 2) reshaping dei flussi passivi
    cf_df = pl.DataFrame({
        "bucket_year": np.arange(1, len(inp.cf_liab) + 1),
        "cashflow": np.asarray(inp.cf_liab, dtype=float),
    })
    reshaped = reshape_with_lapse(cf_df, lapse, base_lapse=inp.l_base)
    cf_liab_dyn = reshaped["cashflow"].to_numpy()

    # 3) attualizzazione attiva: quota sovrana su rf + spread
    w = (np.zeros(len(inp.cf_asset)) if inp.sovereign_weight is None
         else np.asarray(inp.sovereign_weight, dtype=float))
    curve_asset = np.asarray(inp.curve_rf[:len(inp.cf_asset)], dtype=float) \
        + w * inp.spread_btp
    a_dyn = float(np.sum(
        np.asarray(inp.cf_asset) / (1 + curve_asset)
        ** np.arange(1, len(inp.cf_asset) + 1)))

    # 4) attualizzazione passiva: solo curva risk-free (BEL scontato a rf)
    curve_l = np.asarray(inp.curve_rf[:len(cf_liab_dyn)], dtype=float)
    bel_dyn = float(np.sum(
        cf_liab_dyn / (1 + curve_l) ** np.arange(1, len(cf_liab_dyn) + 1)))

    dur_base = macaulay_duration(np.asarray(inp.cf_liab), inp.base_rate)
    dur_dyn = macaulay_duration(cf_liab_dyn, inp.base_rate)

    return DynamicEngineOutput(
        lapse_rate=lapse,
        a_dyn=a_dyn, bel_dyn=bel_dyn,
        of_pre_liq=a_dyn - bel_dyn,
        liab_duration_dyn=dur_dyn,
        liab_duration_base=dur_base,
        cf_liab_reshaped=cf_liab_dyn,
    )

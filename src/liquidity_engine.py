"""Liquidity engine: fabbisogno di cassa anno 1 e costo delle fire sales.

Formule (modelspec.md, sezione 5):
    Shortfall_1 = max(0, CF~_1^L - CF_1^A - B_0)
    V_sell      = Shortfall_1 * (1 + h)
    C_liq       = V_sell - Shortfall_1 = Shortfall_1 * h

Proprieta' di coerenza:
  - shortfall = 0 oppure h = 0  =>  C_liq = 0
  - shortfall > 0 e h > 0       =>  C_liq > 0
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class LiquidityEngineInput:
    cf_liab_stressed: np.ndarray   # flussi passivi post-lapse
    cf_asset: np.ndarray           # flussi attivi baseline
    cash_buffer: float = 0.0       # B_0, riserve liquide
    haircut: float = 0.02          # h: costo di liquidazione per unita' venduta
    horizon_years: int = 1         # finestra del fabbisogno (MVP: anno 1)


@dataclass(frozen=True)
class LiquidityEngineOutput:
    shortfall: float
    v_sell: float
    c_liq: float
    liquidity_ratio: float  # (CF_in + buffer) / fabbisogno; inf se coperto


def run_liquidity_engine(inp: LiquidityEngineInput) -> LiquidityEngineOutput:
    h = max(0.0, inp.haircut)

    out_n = min(inp.horizon_years, len(inp.cf_liab_stressed))
    cf_out = float(np.sum(np.asarray(inp.cf_liab_stressed[:out_n])))
    cf_in = float(np.sum(np.asarray(inp.cf_asset[:out_n]))) \
        if len(inp.cf_asset) else 0.0

    need = cf_out - cf_in
    if need <= 0:
        return LiquidityEngineOutput(
            shortfall=0.0, v_sell=0.0, c_liq=0.0,
            liquidity_ratio=float("inf"),
        )

    covered = min(need, inp.cash_buffer)
    shortfall = need - covered
    v_sell = shortfall * (1 + h)
    c_liq = v_sell - shortfall

    ratio = (cf_in + inp.cash_buffer) / need if need > 0 else float("inf")
    return LiquidityEngineOutput(
        shortfall=shortfall, v_sell=v_sell, c_liq=c_liq,
        liquidity_ratio=ratio,
    )

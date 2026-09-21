"""Test di coerenza logica dei motori (Fase 3 del piano).

I 5 test minimi:
  1. gamma = 0  =>  lapse dinamico == lapse base
  2. shock nulli  =>  statico e dinamico convergono
  3. dr > 0  =>  il valore di un portafoglio obbligazionario lungo scende
  4. riscatti maggiori  =>  liability duration dinamica piu' corta
  5. fabbisogno > buffer  =>  costo di liquidazione positivo

Se questi test non passano, la dashboard e' irrilevante.
"""

from datetime import date

import numpy as np
import polars as pl
import pytest

from src.cashflow_builder import (
    build_asset_cashflows, build_liability_cashflows, reshape_with_lapse,
    total_assets_from_sfcr,
)
from src.metrics import (
    present_value, modified_duration, convexity, macaulay_duration,
)
from src.static_engine import run_static_engine, StaticEngineInput
from src.dynamic_engine import run_dynamic_engine, DynamicEngineInput, calculate_lapse_rate
from src.liquidity_engine import run_liquidity_engine, LiquidityEngineInput
from src.sps_calculator import calculate_sps, SPSInput

T = 10
BEL = 48000.0
DUR_L = 8.8
DUR_A = 6.2
R = 0.02
GAMMA = 0.35


@pytest.fixture(scope="module")
def cf_liab() -> np.ndarray:
    df = build_liability_cashflows(BEL, DUR_L, tenor=T, base_rate=R)
    return df["cashflow"].to_numpy()


@pytest.fixture(scope="module")
def cf_asset() -> np.ndarray:
    assets = BEL + 5600.0
    df = build_asset_cashflows(assets, DUR_A, btp_share=0.35,
                               tenor=T, base_rate=R)
    # aggrega per bucket (il builder separa sovrano/non-sovrano)
    return (df.group_by("bucket_year")
              .agg(pl.col("cashflow").sum())
              .sort("bucket_year")["cashflow"].to_numpy())


def flat_curve(rate: float, n: int = T) -> np.ndarray:
    return np.full(n, rate)


# ---------- Test 1: gamma = 0 ----------

def test_gamma_zero_lapse_equals_base():
    assert calculate_lapse_rate(0.05, 0.05, 0.01, gamma=0.0) == 0.05


def test_gamma_zero_reshaping_is_identity(cf_liab):
    df = pl.DataFrame({
        "bucket_year": np.arange(1, T + 1), "cashflow": cf_liab,
    })
    out = reshape_with_lapse(df, lapse_rate=0.05, base_lapse=0.05)
    np.testing.assert_allclose(out["cashflow"].to_numpy(), cf_liab)


# ---------- Test 2: shock nulli => convergenza ----------

def test_no_shock_static_equals_dynamic(cf_asset, cf_liab):
    static = run_static_engine(StaticEngineInput(cf_asset, cf_liab,
                                                 base_rate=R, delta_rf_bps=0.0))
    dyn = run_dynamic_engine(DynamicEngineInput(
        cf_asset=cf_asset, cf_liab=cf_liab,
        curve_rf=flat_curve(R), spread_btp=0.0, gamma=0.0,
    ))
    # entrambi attualizzano sulla stessa curva piatta senza lapse
    np.testing.assert_allclose(static.a_0, dyn.a_dyn, rtol=1e-8)
    np.testing.assert_allclose(static.bel_0, dyn.bel_dyn, rtol=1e-8)


# ---------- Test 3: dr > 0 => attivo lungo scende ----------

def test_rate_shock_reduces_asset_value(cf_asset, cf_liab):
    base = run_static_engine(StaticEngineInput(cf_asset, cf_liab,
                                               base_rate=R, delta_rf_bps=0.0))
    stressed = run_static_engine(StaticEngineInput(cf_asset, cf_liab,
                                                   base_rate=R, delta_rf_bps=250.0))
    assert stressed.a_stat < base.a_stat

    # anche il PV puro su curva shockata scende
    pv_base = present_value(cf_asset, R)
    pv_up = present_value(cf_asset, R + 0.025)
    assert pv_up < pv_base


# ---------- Test 4: lapse aumenta => duration passiva scende ----------

def test_lapse_shortens_liability_duration(cf_liab):
    df = pl.DataFrame({
        "bucket_year": np.arange(1, T + 1), "cashflow": cf_liab,
    })
    low = reshape_with_lapse(df, 0.05)["cashflow"].to_numpy()
    high = reshape_with_lapse(df, 0.35)["cashflow"].to_numpy()
    assert macaulay_duration(high, R) < macaulay_duration(low, R)


def test_dynamic_engine_duration_shortens_with_gamma(cf_asset, cf_liab):
    base = run_dynamic_engine(DynamicEngineInput(
        cf_asset, cf_liab, flat_curve(R), gamma=0.0))
    stressed = run_dynamic_engine(DynamicEngineInput(
        cf_asset, cf_liab, flat_curve(R), gamma=GAMMA,
        r_mkt=0.045, r_port=0.01, c_fric=0.01))
    assert stressed.liab_duration_dyn < base.liab_duration_dyn


# ---------- Test 5: shortfall > 0 e h > 0 => C_liq > 0 ----------

def test_liquidity_cost_positive_on_shortfall():
    out = run_liquidity_engine(LiquidityEngineInput(
        cf_liab_stressed=np.array([5000.0] + [0.0] * 9),
        cf_asset=np.array([1000.0] + [0.0] * 9),
        cash_buffer=500.0, haircut=0.03,
    ))
    assert out.shortfall > 0
    assert out.c_liq > 0
    np.testing.assert_allclose(out.c_liq, out.shortfall * 0.03)


def test_no_shortfall_no_cost():
    out = run_liquidity_engine(LiquidityEngineInput(
        cf_liab_stressed=np.array([1000.0, 0.0]),
        cf_asset=np.array([2000.0, 0.0]),
        cash_buffer=0.0, haircut=0.03,
    ))
    assert out.c_liq == 0.0
    assert out.shortfall == 0.0


def test_zero_haircut_zero_cost():
    out = run_liquidity_engine(LiquidityEngineInput(
        cf_liab_stressed=np.array([5000.0, 0.0]),
        cf_asset=np.array([0.0, 0.0]),
        cash_buffer=0.0, haircut=0.0,
    ))
    assert out.shortfall > 0 and out.c_liq == 0.0


# ---------- proprieta' dei cash flow sintetici ----------

def test_synthetic_liab_matches_bel_and_duration(cf_liab):
    np.testing.assert_allclose(present_value(cf_liab, R), BEL, rtol=1e-4)
    assert abs(macaulay_duration(cf_liab, R) - DUR_L) < 0.15


def test_synthetic_assets_match_total(cf_asset):
    total = BEL + 5600.0
    np.testing.assert_allclose(present_value(cf_asset, R), total, rtol=1e-4)


# ---------- SPS ----------

def test_sps_bounds_and_monotonicity():
    low = calculate_sps(SPSInput(
        of_stat=5600.0, of_dyn=5600.0, c_liq=0.0,
        own_funds_base=5600.0, solvency_ratio_stressed=1.3))
    high = calculate_sps(SPSInput(
        of_stat=5600.0, of_dyn=3000.0, c_liq=800.0,
        own_funds_base=5600.0, solvency_ratio_stressed=0.7))
    assert 0.0 <= low[0] <= 1.0
    assert high[0] > low[0]


# ---------- coerenza end-to-end (mini backtest) ----------

def test_end_to_end_pipeline(cf_asset, cf_liab):
    """Statico vs dinamico su scenario Q3 2022-like."""
    delta_bps, spread_bps = 250.0, 230.0
    static = run_static_engine(StaticEngineInput(
        cf_asset, cf_liab, base_rate=R, delta_rf_bps=delta_bps))
    dyn = run_dynamic_engine(DynamicEngineInput(
        cf_asset, cf_liab, flat_curve(R + delta_bps / 10_000.0),
        spread_btp=spread_bps / 10_000.0,
        sovereign_weight=np.full(T, 0.35),
        gamma=GAMMA, r_mkt=0.045, r_port=0.01, c_fric=0.01,
    ))
    liq = run_liquidity_engine(LiquidityEngineInput(
        cf_liab_stressed=dyn.cf_liab_reshaped, cf_asset=cf_asset,
        cash_buffer=450.0, haircut=0.02,
    ))
    of_dyn = dyn.of_pre_liq - liq.c_liq
    blind_spot = static.of_stat - of_dyn
    # il framework produce un delta finito e plausibile (segno NON presupposto)
    assert np.isfinite(blind_spot)

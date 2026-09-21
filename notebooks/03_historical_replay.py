# Notebook 3 - Historical Replay
# Esegue gli scenari Q3/Q4 2022 su ogni compagnia, confronta statico vs
# dinamico e produce results_backtest. SOLO dopo che notebook 1 e i
# test di coerenza sono verdi.

# %%
from datetime import date
from pathlib import Path

import numpy as np
import polars as pl

from src.data_loader import load_all, join_scenario_with_company
from src.data_quality import run_quality_checks
from src.cashflow_builder import (
    build_asset_cashflows, build_liability_cashflows, total_assets_from_sfcr,
)
from src.static_engine import StaticEngineInput, run_static_engine
from src.dynamic_engine import DynamicEngineInput, run_dynamic_engine
from src.liquidity_engine import LiquidityEngineInput, run_liquidity_engine
from src.sps_calculator import calculate_sps, SPSInput, sps_label

R = 0.02            # tasso base per i profili sintetici
TENOR = 10
HAIRCUT = 0.02

# %%
tables = load_all(Path("data/processed"))
report = run_quality_checks(tables)
print(report.summary())
assert not report.has_errors, "Data quality FAILED: vedere notebook 1."

company = tables["company_sfcr"]
scenarios = tables["stress_scenarios"]
panel = join_scenario_with_company(company, scenarios)

# %% [markdown]
# ## Loop compagnia x scenario
# NOTA METODOLOGICA: il motore dinamico e' costruito per verificare se e in
# che misura le non linearita' producano vulnerabilita' aggiuntiva. Il segno
# e l'entita' del blind spot sono un output, non un presupposto.

# %%
results = []
for row in panel.iter_rows(named=True):
    cf_l = build_liability_cashflows(
        bel=row["bel"], liability_duration=row["liability_duration"],
        tenor=TENOR, base_rate=R,
        company_id=row["company_id"], report_date=row["report_date"],
    )["cashflow"].to_numpy()

    assets = total_assets_from_sfcr(row)
    cf_a_df = build_asset_cashflows(
        total_assets=assets, asset_duration=row["asset_duration"],
        btp_share=row["btp_share"] or 0.0, tenor=TENOR, base_rate=R,
        company_id=row["company_id"], report_date=row["report_date"],
    )
    cf_a = (cf_a_df.group_by("bucket_year")
                  .agg(pl.col("cashflow").sum())
                  .sort("bucket_year")["cashflow"].to_numpy())

    delta = row["delta_rf_bps"] / 10_000.0
    curve = np.full(TENOR, R + delta)

    static = run_static_engine(StaticEngineInput(
        cf_a, cf_l, base_rate=R, delta_rf_bps=row["delta_rf_bps"]))
    dyn = run_dynamic_engine(DynamicEngineInput(
        cf_a, cf_l, curve,
        spread_btp=row["spread_btp_bps"] / 10_000.0,
        sovereign_weight=np.full(TENOR, row["btp_share"] or 0.0),
        gamma=row["lapse_gamma"],
        r_mkt=0.045, r_port=0.01, c_fric=0.01,
    ))
    liq = run_liquidity_engine(LiquidityEngineInput(
        cf_liab_stressed=dyn.cf_liab_reshaped, cf_asset=cf_a,
        cash_buffer=row["cash_buffer"] or 0.0, haircut=HAIRCUT,
    ))

    of_dyn = dyn.of_pre_liq - liq.c_liq
    blind_spot = static.of_stat - of_dyn
    ratio_stress = of_dyn / row["scr"] if of_dyn > 0 else 0.0
    sps, comps = calculate_sps(SPSInput(
        of_stat=static.of_stat, of_dyn=of_dyn, c_liq=liq.c_liq,
        own_funds_base=row["own_funds"],
        solvency_ratio_stressed=ratio_stress))

    results.append({
        "company_id": row["company_id"],
        "scenario_id": row["scenario_id"],
        "a_stat": static.a_stat, "bel_stat": static.bel_stat,
        "of_stat": static.of_stat,
        "a_dyn": dyn.a_dyn, "bel_dyn": dyn.bel_dyn, "of_dyn": of_dyn,
        "c_liq": liq.c_liq,
        "blind_spot_delta": blind_spot,
        "sps": sps, "sps_label": sps_label(sps),
        "lapse_rate": dyn.lapse_rate,
        "solvency_ratio_stressed": ratio_stress,
    })

res = pl.DataFrame(results)

# %% [markdown]
# ## Risultati: confronto statico vs dinamico

# %%
cols = ["company_id", "scenario_id", "of_stat", "of_dyn",
        "blind_spot_delta", "c_liq", "sps", "sps_label"]
print(res.select(cols).sort("company_id", "scenario_id"))

# %% [markdown]
# ## Decomposizione del blind spot (per il waterfall)

# %%
decomp = res.with_columns(
    (pl.col("bel_dyn") - pl.col("bel_stat")).alias("lapse_effect"),
    (pl.col("a_stat") - pl.col("a_dyn") - pl.col("c_liq"))
        .alias("mtm_spread_effect"),
).select(["company_id", "scenario_id", "lapse_effect",
          "mtm_spread_effect", "c_liq", "blind_spot_delta"])
print(decomp.sort("company_id", "scenario_id"))

# %% [markdown]
# ## Salvataggio in data/processed/results_backtest

# %%
out = Path("data/processed")
out.mkdir(parents=True, exist_ok=True)
res.write_parquet(out / "results_backtest.parquet")
res.write_csv(out / "results_backtest.csv")
print(f"salvate {res.height} righe")

# %% [markdown]
# ## Checklist di uscita
# - [ ] nessun ERROR nel data quality
# - [ ] test di coerenza (tests/test_model_coherence.py) verdi
# - [ ] scenario BASE: |blind_spot| ~ 0 (entro tolleranza)
# - [ ] risultati salvati e replicabili (seed/notebook versionato)

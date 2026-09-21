"""Dashboard ALM Dynamic Audit (Streamlit).

Consuma SOLO funzioni gia' validate da tests/ e notebooks/:
nessuna logica di modellazione vive qui. Ogni modifica al motore
passa prima da pytest e dal Notebook 3.

Esecuzione: streamlit run app/app.py
"""

from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import polars as pl
import streamlit as st

from src.data_loader import load_all
from src.data_quality import run_quality_checks
from src.cashflow_builder import (
    build_asset_cashflows, build_liability_cashflows,
    total_assets_from_sfcr,
)
from src.static_engine import StaticEngineInput, run_static_engine
from src.dynamic_engine import DynamicEngineInput, run_dynamic_engine
from src.liquidity_engine import LiquidityEngineInput, run_liquidity_engine
from src.sps_calculator import calculate_sps, SPSInput, sps_label

R = 0.02
TENOR = 10

st.set_page_config(page_title="ALM Dynamic Audit", layout="wide")
st.title("ALM Dynamic Audit - Statico vs Dinamico")
st.caption(
    "Il motore dinamico e' costruito per verificare se e in quale misura "
    "non linearita', spread e riscatti endogeni producano vulnerabilita' "
    "aggiuntiva rispetto al benchmark statico. Il segno del delta e' un "
    "output, non un presupposto."
)

# ---------------------------------------------------------------- data

@st.cache_data(ttl=300)
def load_data() -> dict[str, pl.DataFrame]:
    return load_all(Path("data/processed"))


@st.cache_data(ttl=300)
def load_results() -> pl.DataFrame:
    p = Path("data/processed/results_backtest.parquet")
    if p.exists():
        return pl.read_parquet(p)
    return pl.DataFrame()


tables = load_data()
report = run_quality_checks(tables)

with st.expander(f"Data quality - {report.summary()}", expanded=False):
    if report.violations:
        st.dataframe(pd.DataFrame([
            {"severity": v.severity, "table": v.table, "column": v.column,
             "message": v.message} for v in report.violations
        ]))
    else:
        st.success("Nessuna violazione.")
    if report.has_errors:
        st.error("ERROR presenti: la dashboard resta consultabile ma i "
                 "risultati non sono attendibili.")
        st.stop()

company = tables["company_sfcr"]
scenarios = tables["stress_scenarios"]
if company.height == 0:
    st.warning("Nessuna compagnia caricata in data/processed/.")
    st.stop()

# ---------------------------------------------------------------- sidebar

st.sidebar.header("Parametri di stress")

comp_ids = sorted(company["company_id"].unique().to_list())
company_id = st.sidebar.selectbox("Compagnia", comp_ids)

scenario_ids = (["- nessuno (parametri liberi)"]
                + scenarios["scenario_id"].to_list())
scenario_id = st.sidebar.selectbox("Scenario storico", scenario_ids)

delta_rf_bps = st.sidebar.slider("Shift curva tassi (bps)", -100, 500, 250, 10)
spread_bps = st.sidebar.slider("Shock spread BTP (bps)", 0, 500, 230, 10)
gamma = st.sidebar.slider("Sensibilita' riscatti (gamma)", 0.0, 1.5, 0.35, 0.05)
haircut = st.sidebar.slider("Haircut di liquidazione", 0.0, 0.10, 0.02, 0.005)
lapse_cap = st.sidebar.slider("Cap lapse L_max", 0.10, 0.80, 0.40, 0.05)
cash_buffer = st.sidebar.number_input(
    "Cash buffer (mln)", min_value=0.0, value=450.0, step=50.0)

# preset dallo scenario storico
if scenario_id != "- nessuno (parametri liberi)":
    sc = scenarios.filter(pl.col("scenario_id") == scenario_id).row(0, named=True)
    delta_rf_bps = int(sc["delta_rf_bps"])
    spread_bps = int(sc["spread_btp_bps"])
    gamma = float(sc["lapse_gamma"])
    st.sidebar.info(f"Preset {sc['label']}: drf {delta_rf_bps}bps, "
                    f"spread {spread_bps}bps, gamma {gamma}")

# ---------------------------------------------------------------- engine

row = (company.filter(pl.col("company_id") == company_id)
              .sort("report_date").row(-1, named=True))

cf_l_df = build_liability_cashflows(
    bel=row["bel"], liability_duration=row["liability_duration"] or 8.0,
    tenor=TENOR, base_rate=R)
cf_l = cf_l_df["cashflow"].to_numpy()

assets = total_assets_from_sfcr(row)
cf_a_df = build_asset_cashflows(
    total_assets=assets, asset_duration=row["asset_duration"] or 6.0,
    btp_share=row["btp_share"] or 0.0, tenor=TENOR, base_rate=R)
cf_a = (cf_a_df.group_by("bucket_year")
              .agg(pl.col("cashflow").sum())
              .sort("bucket_year")["cashflow"].to_numpy())

btp_w = row["btp_share"] or 0.0
curve = np.full(TENOR, R + delta_rf_bps / 10_000.0)

static = run_static_engine(StaticEngineInput(
    cf_a, cf_l, base_rate=R, delta_rf_bps=float(delta_rf_bps)))
dyn = run_dynamic_engine(DynamicEngineInput(
    cf_a, cf_l, curve,
    spread_btp=spread_bps / 10_000.0,
    sovereign_weight=np.full(TENOR, btp_w),
    gamma=gamma, r_mkt=0.045, r_port=0.01, c_fric=0.01,
    l_max=lapse_cap,
))
liq = run_liquidity_engine(LiquidityEngineInput(
    cf_liab_stressed=dyn.cf_liab_reshaped, cf_asset=cf_a,
    cash_buffer=cash_buffer, haircut=haircut,
))

of_dyn = dyn.of_pre_liq - liq.c_liq
blind_spot = static.of_stat - of_dyn
ratio_stress = of_dyn / row["scr"] if of_dyn > 0 else 0.0
sps, comps = calculate_sps(SPSInput(
    of_stat=static.of_stat, of_dyn=of_dyn, c_liq=liq.c_liq,
    own_funds_base=row["own_funds"],
    solvency_ratio_stressed=ratio_stress))

# ---------------------------------------------------------------- KPI

st.subheader(f"{row['company_name']} - report {row['report_date']} "
             f"(BEL {row['bel']:,.0f} mln, OF {row['own_funds']:,.0f} mln)")

k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("OF statici", f"{static.of_stat:,.0f} mln")
k2.metric("OF dinamici", f"{of_dyn:,.0f} mln",
          f"{of_dyn - static.of_stat:,.0f}")
k3.metric("Delta blind spot", f"{blind_spot:,.0f} mln")
k4.metric("Ratio stressata", f"{ratio_stress:.2f}",
          f"{ratio_stress - row['solvency_ratio']:+.2f}")
k5.metric("SPS", f"{sps:.3f} ({sps_label(sps)})")

st.caption(f"Lapse endogeno stimato: {dyn.lapse_rate:.1%} | "
           f"Costo liquidazione: {liq.c_liq:,.0f} mln | "
           f"Liquidity ratio: {liq.liquidity_ratio:.2f}")

# ---------------------------------------------------------------- grafici

tab_div, tab_wf, tab_sps, tab_cf = st.tabs(
    ["Divergenza", "Waterfall", "SPS", "Cash flow & curva"])

# --- divergenza: sweep del shift tassi, statico vs dinamico
with tab_div:
    sweep = np.linspace(0, 500, 26)
    of_stat_line, of_dyn_line = [], []
    for bps in sweep:
        s = run_static_engine(StaticEngineInput(
            cf_a, cf_l, base_rate=R, delta_rf_bps=float(bps)))
        d = run_dynamic_engine(DynamicEngineInput(
            cf_a, cf_l, np.full(TENOR, R + bps / 10_000.0),
            spread_btp=spread_bps / 10_000.0,
            sovereign_weight=np.full(TENOR, btp_w),
            gamma=gamma, r_mkt=0.045, r_port=0.01, c_fric=0.01,
            l_max=lapse_cap))
        l = run_liquidity_engine(LiquidityEngineInput(
            cf_liab_stressed=d.cf_liab_reshaped, cf_asset=cf_a,
            cash_buffer=cash_buffer, haircut=haircut))
        of_stat_line.append(s.of_stat)
        of_dyn_line.append(d.of_pre_liq - l.c_liq)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=sweep, y=of_stat_line, name="OF statici (benchmark lineare)",
        mode="lines", line=dict(dash="dash")))
    fig.add_trace(go.Scatter(
        x=sweep, y=of_dyn_line, name="OF dinamici (M2M + lapse + liquidita')",
        mode="lines"))
    fig.add_vline(x=delta_rf_bps, line_dash="dot",
                  annotation_text="scenario corrente")
    fig.update_layout(
        title="Own Funds al variare dello shift tassi",
        xaxis_title="Shift curva (bps)", yaxis_title="Own Funds (mln)")
    st.plotly_chart(fig, use_container_width=True)

# --- waterfall della decomposizione
with tab_wf:
    a_dyn_no_spread = run_dynamic_engine(DynamicEngineInput(
        cf_a, cf_l, curve, spread_btp=0.0,
        sovereign_weight=np.full(TENOR, btp_w),
        gamma=gamma, r_mkt=0.045, r_port=0.01, c_fric=0.01,
        l_max=lapse_cap))
    spread_effect = a_dyn_no_spread.a_dyn - dyn.a_dyn
    lapse_effect = dyn.bel_dyn - static.bel_stat
    liq_effect = -liq.c_liq

    fig = go.Figure(go.Waterfall(
        orientation="v",
        measure=["absolute", "relative", "relative", "relative", "relative",
                 "total"],
        x=["OF statici", "Convexity/spread (attivi)", "Lapse endogeno",
           "Costi liquidazione", "OF dinamici", "Delta blind spot"],
        y=[static.of_stat, spread_effect, -lapse_effect, liq_effect,
           of_dyn, blind_spot],
        textposition="outside",
        connector={"line": {"color": "grey"}},
    ))
    fig.update_layout(title="Decomposizione: da OF statici a OF dinamici",
                      yaxis_title="mln")
    st.plotly_chart(fig, use_container_width=True)

# --- componenti SPS
with tab_sps:
    fig = go.Figure(go.Bar(
        x=["Blind spot / OF", "C_liq / OF", "Solvency < 1"],
        y=[comps["delta"], comps["liq"], comps["solv"]],
        marker_color=["#d62728", "#ff7f0e", "#1f77b4"],
    ))
    fig.add_hline(y=sps, line_dash="dot",
                  annotation_text=f"SPS = {sps:.3f}")
    fig.update_layout(title=f"Componenti SPS - {sps_label(sps)}",
                      yaxis_title="contributo (0-1)", yaxis_range=[0, 1])
    st.plotly_chart(fig, use_container_width=True)

    results = load_results()
    if results.height:
        st.dataframe(results.filter(
            pl.col("company_id") == company_id
        ).sort("scenario_id").to_pandas(), use_container_width=True)
    else:
        st.info("Nessun results_backtest salvato: eseguire il Notebook 3.")

# --- profili e curva
with tab_cf:
    c1, c2 = st.columns(2)
    with c1:
        fig = go.Figure()
        x = list(range(1, TENOR + 1))
        fig.add_trace(go.Bar(x=x, y=cf_a, name="attivi"))
        fig.add_trace(go.Bar(x=x, y=dyn.cf_liab_reshaped,
                             name="passivi (post-lapse)"))
        fig.add_trace(go.Bar(x=x, y=cf_l, name="passivi base", opacity=0.35))
        fig.update_layout(barmode="group",
                          title="Cash flow sintetici (flag E)",
                          xaxis_title="anno", yaxis_title="mln")
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=x, y=(curve * 100), name="curva rf stressata"))
        fig.add_trace(go.Scatter(
            x=x, y=(curve + btp_w * spread_bps / 10_000.0) * 100,
            name=f"attivi sovrani ({btp_w:.0%} quota, spread)"))
        fig.update_layout(title="Curve di sconto",
                          xaxis_title="scadenza", yaxis_title="tasso (%)")
        st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------------------- audit

with st.expander("Audit trail", expanded=False):
    st.json({
        "company_id": company_id, "report_date": str(row["report_date"]),
        "scenario": scenario_id,
        "params": {"delta_rf_bps": delta_rf_bps, "spread_bps": spread_bps,
                   "gamma": gamma, "haircut": haircut,
                   "lapse_cap": lapse_cap, "cash_buffer": cash_buffer},
        "outputs": {
            "of_stat": round(static.of_stat, 1),
            "of_dyn": round(of_dyn, 1),
            "blind_spot_delta": round(blind_spot, 1),
            "c_liq": round(liq.c_liq, 1),
            "lapse_rate": round(dyn.lapse_rate, 4),
            "sps": round(sps, 4),
            "sps_components": {k: round(v, 4) for k, v in comps.items()},
        },
        "data_quality": report.summary(),
    })

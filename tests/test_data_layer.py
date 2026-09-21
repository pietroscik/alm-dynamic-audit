"""Test del layer dati: types, data_loader, data_quality.

Esecuzione: pytest tests/ -v
"""

from datetime import date
from pathlib import Path

import polars as pl
import pytest

from src.data_loader import load_table, load_all, join_scenario_with_company
from src.data_quality import (
    run_quality_checks, QualityReport, check_ode_values, VALID_ODE,
)
from src.types import CompanySFCR, StressScenario, ODE


# ---------- fixture: tabelle sintetiche pulite ----------

@pytest.fixture
def company_sfcr_ok() -> pl.DataFrame:
    return pl.DataFrame({
        "company_id": ["C01", "C01", "C02", "C02"],
        "company_name": ["Alpha Vita", "Alpha Vita", "Beta Assicura", "Beta Assicura"],
        "report_date": [date(2021, 12, 31), date(2022, 12, 31),
                        date(2021, 12, 31), date(2022, 12, 31)],
        "bel": [50000.0, 48000.0, 20000.0, 19500.0],
        "own_funds": [6000.0, 5600.0, 2500.0, 2400.0],
        "scr": [4500.0, 4300.0, 1900.0, 1850.0],
        "solvency_ratio": [1.333, 1.302, 1.316, 1.297],
        "btp_share": [0.35, 0.38, 0.25, 0.27],
        "asset_duration": [6.5, 6.2, 5.0, 4.8],
        "liability_duration": [9.0, 8.8, 7.5, 7.3],
        "cash_buffer": [500.0, 450.0, 200.0, 190.0],
        "source_doc": ["sfcr_alpha_2021.pdf"] * 4,
        "source_page": ["p. 45"] * 4,
        "quality_flag": ["complete"] * 4,
    })


@pytest.fixture
def macro_series_ok() -> pl.DataFrame:
    return pl.DataFrame({
        "obs_date": [date(2022, 9, 30), date(2022, 9, 30),
                     date(2022, 12, 31), date(2022, 12, 31)],
        "country": ["IT", "DE", "IT", "DE"],
        "series_name": ["btp_10y", "bund_10y", "btp_10y", "bund_10y"],
        "value": [4.45, 2.15, 4.65, 2.37],
        "source": ["BCE"] * 4,
        "obs_flag": ["O"] * 4,
    })


@pytest.fixture
def stress_scenarios_ok() -> pl.DataFrame:
    return pl.DataFrame({
        "scenario_id": ["BASE", "Q3_2022", "Q4_2022"],
        "scenario_date": [date(2022, 6, 30), date(2022, 9, 30),
                          date(2022, 12, 31)],
        "delta_rf_bps": [0.0, 250.0, 320.0],
        "spread_btp_bps": [0.0, 230.0, 235.0],
        "inflation_yoy": [8.0, 8.9, 11.8],
        "lapse_gamma": [0.0, 0.35, 0.40],
        "label": ["Baseline", "Q3 2022", "Q4 2022"],
    })


@pytest.fixture
def tables_ok(company_sfcr_ok, macro_series_ok, stress_scenarios_ok):
    return {
        "company_sfcr": company_sfcr_ok,
        "macro_series": macro_series_ok,
        "stress_scenarios": stress_scenarios_ok,
    }


# ---------- data_quality ----------

def test_quality_passes_on_clean_data(tables_ok):
    report = run_quality_checks(tables_ok)
    assert not report.has_errors, [v.message for v in report.violations]


def test_null_company_id_fails(company_sfcr_ok):
    df = company_sfcr_ok.with_columns(
        pl.when(pl.int_range(pl.len()) == 0)
        .then(None).otherwise(pl.col("company_id")).alias("company_id")
    )
    report = run_quality_checks({"company_sfcr": df})
    assert report.has_errors
    assert any("company_id" in (v.column or "") for v in report.violations)


def test_negative_bel_fails(company_sfcr_ok):
    df = company_sfcr_ok.with_columns(
        pl.when(pl.int_range(pl.len()) == 0)
        .then(-1.0).otherwise(pl.col("bel")).alias("bel")
    )
    report = run_quality_checks({"company_sfcr": df})
    assert report.has_errors


def test_btp_share_in_pct_fails(company_sfcr_ok):
    df = company_sfcr_ok.with_columns((pl.col("btp_share") * 100).alias("btp_share"))
    report = run_quality_checks({"company_sfcr": df})
    assert any(v.column == "btp_share" and v.severity == "ERROR"
               for v in report.violations)


def test_ode_mixed_flag_rejected():
    df = pl.DataFrame({"obs_flag": ["O", "E/O", "O"]})
    report = QualityReport()
    check_ode_values(df, "macro_series", "obs_flag", report)
    assert report.has_errors


def test_duplicate_company_year_fails(company_sfcr_ok):
    df = pl.concat([company_sfcr_ok, company_sfcr_ok.head(1)])
    report = run_quality_checks({"company_sfcr": df})
    assert report.has_errors


def test_inconsistent_solvency_ratio_warns(company_sfcr_ok):
    df = company_sfcr_ok.with_columns((pl.col("solvency_ratio") + 0.5)
                                      .alias("solvency_ratio"))
    report = run_quality_checks({"company_sfcr": df})
    assert not report.has_errors  # solo WARN
    assert any(v.severity == "WARN" and v.column == "solvency_ratio"
               for v in report.violations)


# ---------- data_loader ----------

def test_load_table_csv(tmp_path: Path, company_sfcr_ok):
    f = tmp_path / "company_sfcr.csv"
    # salviamo con nomi "sorgente" per testare la normalizzazione
    raw = company_sfcr_ok.rename({
        "company_id": "CompanyId", "own_funds": "ownfundsreported",
        "scr": "scrreported", "bel": "belreported",
    })
    raw.write_csv(f)
    df = load_table(f, "company_sfcr")
    assert {"company_id", "own_funds", "scr", "bel"} <= set(df.columns)
    assert df.height == 4
    assert df.schema["bel"] == pl.Float64


def test_load_table_missing_columns_raises(tmp_path: Path):
    f = tmp_path / "bad.csv"
    f.write_text("company_id,report_date\nC01,2022-12-31\n")
    with pytest.raises(ValueError, match="colonne mancanti"):
        load_table(f, "company_sfcr")


def test_load_table_missing_file_raises(tmp_path: Path):
    with pytest.raises(ValueError, match="File non trovato"):
        load_table(tmp_path / "nope.csv", "company_sfcr")


def test_load_all_empty_dir(tmp_path: Path):
    tables = load_all(tmp_path)
    assert set(tables) == {"company_sfcr", "macro_series", "stress_scenarios"}
    assert all(df.height == 0 for df in tables.values())


def test_cross_join_scenario_company(company_sfcr_ok, stress_scenarios_ok):
    out = join_scenario_with_company(company_sfcr_ok, stress_scenarios_ok)
    assert out.height == company_sfcr_ok.height * stress_scenarios_ok.height
    assert "scenario_id" in out.columns and "company_id" in out.columns


# ---------- types ----------

def test_company_sfcr_frozen_and_required():
    c = CompanySFCR(
        company_id="C01", company_name="Alpha Vita",
        report_date=date(2022, 12, 31),
        bel=48000.0, own_funds=5600.0, scr=4300.0,
    )
    assert c.quality_flag == "complete"
    with pytest.raises(Exception):
        c.bel = 1.0  # frozen


def test_scenario_defaults():
    s = StressScenario(scenario_id="X", scenario_date=date(2022, 9, 30),
                       delta_rf_bps=250.0, spread_btp_bps=230.0)
    assert s.lapse_gamma == 0.0
    assert s.label == ""


def test_ode_enum_single_values():
    assert {e.value for e in ODE} == VALID_ODE

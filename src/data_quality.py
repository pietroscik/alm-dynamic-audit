"""Controlli automatici di qualita' sui dati (pre-motori).

Ogni check restituisce una lista di violazioni strutturate.
Severita':
  - ERROR  -> blocca la pipeline,
  - WARN   -> segnala ma non blocca.

La classificazione O/D/E ammette valori singoli in {O, D, E}:
niente flag misti "E/O" o "O/E"; le ambiguita' vanno nel campo
measurement_note del data_dictionary, non nel flag.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import Optional

import polars as pl

VALID_ODE = {"O", "D", "E"}


@dataclass
class Violation:
    table: str
    column: Optional[str]
    severity: str  # ERROR / WARN
    message: str
    n_rows: int = 0


@dataclass
class QualityReport:
    violations: list[Violation] = field(default_factory=list)

    @property
    def has_errors(self) -> bool:
        return any(v.severity == "ERROR" for v in self.violations)

    def summary(self) -> str:
        errors = sum(v.severity == "ERROR" for v in self.violations)
        warns = sum(v.severity == "WARN" for v in self.violations)
        return f"{errors} errori, {warns} warning"

    def raise_if_errors(self) -> None:
        if self.has_errors:
            msgs = "\n".join(
                f"  [{v.table}.{v.column}] {v.message}"
                for v in self.violations if v.severity == "ERROR"
            )
            raise ValueError(f"Data quality FAILED:\n{msgs}")


def check_not_null(
    df: pl.DataFrame, table: str, column: str, report: QualityReport
) -> None:
    if column not in df.columns:
        report.violations.append(
            Violation(table, column, "ERROR", "colonna assente")
        )
        return
    n = df.filter(pl.col(column).is_null()).height
    if n:
        report.violations.append(
            Violation(table, column, "ERROR", f"{n} valori nulli", n)
        )


def check_non_negative(
    df: pl.DataFrame, table: str, columns: list[str],
    report: QualityReport,
) -> None:
    for col in columns:
        if col not in df.columns:
            continue
        n = df.filter(pl.col(col) < 0).height
        if n:
            report.violations.append(
                Violation(table, col, "ERROR", f"{n} valori negativi", n)
            )


def check_ode_values(
    df: pl.DataFrame, table: str, column: str, report: QualityReport
) -> None:
    if column not in df.columns:
        return
    bad = df.filter(~pl.col(column).is_in(list(VALID_ODE)))
    if bad.height:
        report.violations.append(
            Violation(
                table, column, "ERROR",
                f"{bad.height} flag ODE non ammessi "
                f"(valori validi: O, D, E)", bad.height,
            )
        )


def check_company_sfcr(df: pl.DataFrame, report: QualityReport) -> None:
    t = "company_sfcr"
    if df.height == 0:
        report.violations.append(Violation(t, None, "WARN", "tabella vuota"))
        return

    for col in ("company_id", "report_date", "bel", "own_funds", "scr"):
        check_not_null(df, t, col, report)
    check_non_negative(
        df, t, ["bel", "own_funds", "scr", "asset_duration",
                "liability_duration"], report
    )

    # btp_share come frazione (0-1): WARN se in percentuale (0-100)
    if "btp_share" in df.columns:
        n = df.filter(pl.col("btp_share") > 1.5).height
        if n:
            report.violations.append(
                Violation(t, "btp_share", "ERROR",
                          f"{n} valori > 1.5: probabilmente in pct, "
                          f"attesa frazione 0-1", n)
            )

    # date future non hanno senso per un report storico
    if "report_date" in df.columns:
        n = df.filter(pl.col("report_date") > date.today()).height
        if n:
            report.violations.append(
                Violation(t, "report_date", "ERROR",
                          f"{n} date di report nel futuro", n)
            )

    # coerenza interna: ratio dichiarato vs own_funds / scr
    if {"own_funds", "scr", "solvency_ratio"} <= set(df.columns):
        sub = df.drop_nulls(["own_funds", "scr", "solvency_ratio"])
        if sub.height:
            implied = sub["own_funds"] / sub["scr"]
            diff = (implied - sub["solvency_ratio"]).abs()
            n = (diff > 0.05).sum()
            if n:
                report.violations.append(
                    Violation(t, "solvency_ratio", "WARN",
                              f"{n} ratio non coerente con OF/SCR "
                              f"(tolleranza 0.05)", n)
                )

    # duplicati compagnia-anno
    if {"company_id", "report_date"} <= set(df.columns):
        n_dup = df.height - df.select(["company_id", "report_date"]).unique().height
        if n_dup:
            report.violations.append(
                Violation(t, "company_id", "ERROR",
                          f"{n_dup} duplicati compagnia-anno", n_dup)
            )


def check_macro_series(df: pl.DataFrame, report: QualityReport) -> None:
    t = "macro_series"
    if df.height == 0:
        report.violations.append(Violation(t, None, "WARN", "tabella vuota"))
        return
    for col in ("obs_date", "country", "series_name", "value", "source"):
        check_not_null(df, t, col, report)
    check_ode_values(df, t, "obs_flag", report)
    # unita': btp_bund_spread atteso in bps (valore plausibile < 1000)
    if "series_name" in df.columns:
        spread = df.filter(pl.col("series_name") == "btp_bund_spread")
        if spread.height:
            n = spread.filter(pl.col("value").abs() > 1000).height
            if n:
                report.violations.append(
                    Violation(t, "value", "WARN",
                              f"{n} spread > 1000: verificare unita' bps", n)
                )


def check_stress_scenarios(df: pl.DataFrame, report: QualityReport) -> None:
    t = "stress_scenarios"
    if df.height == 0:
        report.violations.append(Violation(t, None, "WARN", "tabella vuota"))
        return
    for col in ("scenario_id", "scenario_date", "delta_rf_bps",
                "spread_btp_bps", "lapse_gamma"):
        check_not_null(df, t, col, report)
    # gamma negativo non ha interpretazione economica
    if "lapse_gamma" in df.columns:
        n = df.filter(pl.col("lapse_gamma") < 0).height
        if n:
            report.violations.append(
                Violation(t, "lapse_gamma", "WARN",
                          f"{n} gamma negativi: verificare calibrazione", n)
            )


def run_quality_checks(
    tables: dict[str, pl.DataFrame],
) -> QualityReport:
    """Esegue tutti i check sulle tabelle caricate e restituisce il report."""
    report = QualityReport()
    checkers = {
        "company_sfcr": check_company_sfcr,
        "macro_series": check_macro_series,
        "stress_scenarios": check_stress_scenarios,
    }
    for name, checker in checkers.items():
        df = tables.get(name)
        if df is None:
            report.violations.append(
                Violation(name, None, "WARN", "tabella non caricata")
            )
            continue
        checker(df, report)
    return report

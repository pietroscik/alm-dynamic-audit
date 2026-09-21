"""Contenitori base per alm-dynamic-audit.

Ogni campo dichiarato qui rispecchia una riga di data_dictionary.csv.
I tipi usano dataclass (nessuna dipendenza esterna); in futuro si puo'
migrare a pydantic senza cambiare i nomi dei campi.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from enum import Enum
from typing import Optional


class ODE(str, Enum):
    """Classificazione del dato: Observed / Estimated / Derived."""

    O = "O"  # osservato da fonte primaria (SFCR, EIOPA, BCE)
    E = "E"  # stimato / proxy
    D = "D"  # derivato dai motori


@dataclass(frozen=True)
class CompanySFCR:
    """Una riga della tabella company_sfcr (una compagnia-anno)."""

    company_id: str
    company_name: str
    report_date: date
    bel: float                                  # O, mln_eur
    own_funds: float                            # O, mln_eur
    scr: float                                  # O, mln_eur
    solvency_ratio: Optional[float] = None      # O/D, pct
    btp_share: Optional[float] = None           # E, pct (0-1)
    asset_duration: Optional[float] = None      # E, anni
    liability_duration: Optional[float] = None  # E, anni
    cash_buffer: Optional[float] = None         # O/E, mln_eur
    source_doc: Optional[str] = None
    source_page: Optional[str] = None
    quality_flag: str = "complete"              # complete / partial


@dataclass(frozen=True)
class MacroObservation:
    """Una riga della tabella macro_series."""

    obs_date: date
    country: str          # IT, DE, EA
    series_name: str      # e.g. btp_10y, bund_10y, inflation_yoy, eiopa_rf
    value: float
    source: str           # BCE, EIOPA, ISTAT
    obs_flag: ODE = ODE.O


@dataclass(frozen=True)
class StressScenario:
    """Una riga della tabella stress_scenarios."""

    scenario_id: str
    scenario_date: date
    delta_rf_bps: float       # shift parallelo equivalente della curva risk-free
    spread_btp_bps: float     # shock spread BTP-Bund
    inflation_yoy: Optional[float] = None
    lapse_gamma: float = 0.0  # sensibilita' riscatti endogeni
    label: str = ""           # es. "Q3 2022"


@dataclass(frozen=True)
class SyntheticCashflowRow:
    """Una riga della tabella synthetic_cashflows."""

    company_id: str
    report_date: date
    side: str              # asset / liability
    bucket_year: int       # 1..T
    cashflow: float        # mln_eur
    discount_curve: str = "rf"  # rf / rf_plus_spread
    ode_flag: ODE = ODE.E


@dataclass
class BacktestResult:
    """Una riga della tabella results_backtest."""

    company_id: str
    scenario_id: str
    of_stat: Optional[float] = None
    bel_stat: Optional[float] = None
    a_stat: Optional[float] = None
    of_dyn: Optional[float] = None
    bel_dyn: Optional[float] = None
    a_dyn: Optional[float] = None
    c_liq: Optional[float] = None
    blind_spot_delta: Optional[float] = None
    sps: Optional[float] = None
    notes: dict = field(default_factory=dict)

"""SPS: punteggio composito di vulnerabilita' prudenziale.

Score in [0, 1] crescente nella vulnerabilita'. Componenti (V1, MVP):
  - w_delta: peso del blind spot normalizzato sugli own funds
  - w_liq:   peso del costo di liquidazione normalizzato sugli own funds
  - w_solv:  peso del ratio stressato sotto 1

Tutti i pesi e le soglie sono in config e vanno dichiarati come [E].
L'SPS e' un indicatore esplorativo di ricerca, NON una misura regulatoria.
"""

from __future__ import annotations

from dataclasses import dataclass

from src.config import SPS_WEIGHTS as WEIGHTS


@dataclass(frozen=True)
class SPSInput:
    of_stat: float
    of_dyn: float
    c_liq: float
    own_funds_base: float
    solvency_ratio_stressed: float  # OF_dyn / SCR


def _clamp01(x: float) -> float:
    return max(0.0, min(1.0, x))


def calculate_sps(inp: SPSInput) -> tuple[float, dict[str, float]]:
    """Ritorna (score, componenti)."""
    of = inp.of_dyn if inp.of_dyn > 0 else max(inp.of_stat, 1e-9)

    # componente 1: blind spot relativo
    comp_delta = _clamp01(
        (inp.of_stat - inp.of_dyn) / max(abs(inp.own_funds_base), 1e-9)
    )
    # componente 2: costo di liquidazione relativo
    comp_liq = _clamp01(inp.c_liq / max(abs(of), 1e-9))
    # componente 3: solvency stressata sotto 100%
    comp_solv = _clamp01(1.0 - inp.solvency_ratio_stressed)

    score = (
        WEIGHTS["delta"] * comp_delta
        + WEIGHTS["liq"] * comp_liq
        + WEIGHTS["solv"] * comp_solv
    )
    components = {
        "delta": comp_delta,
        "liq": comp_liq,
        "solv": comp_solv,
        "weighted": score,
    }
    return score, components


def sps_label(score: float) -> str:
    if score < 0.20:
        return "low"
    if score < 0.40:
        return "moderate"
    if score < 0.60:
        return "elevated"
    return "high"

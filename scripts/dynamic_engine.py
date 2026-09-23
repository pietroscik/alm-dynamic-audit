#!/usr/bin/env python3
"""Dynamic lapse engine — applica la banda di gamma stimata (PVG 2019-2023) alle traiettorie di portafoglio.

Specifica (models/lapse_gamma_stability_pvg.md, §4):
    q_t = q0 * exp(gamma * max(0, ds_{t-1}))
gamma in [19.7, 30.1] per unita' di spread; lag 1 anno; floor a 0 (risposta asimmetrica).

Input: data/interim/lapse_flows_pvg.csv, lapse_flows_pvg_ext.csv (tag [O]/[E-derived]).
Nessun dato inventato: i parametri sono [E-model] tracciati, gli input [O].
"""
from __future__ import annotations
import argparse, math

GAMMA_BAND = {"low": 19.7, "central": 19.7, "high": 30.1}  # per unit of spread (decimal)
LAG = 1  # years


def project_lapse(q0: float, dspread_bps: float, gamma: float) -> float:
    """q_t with asymmetric floor: only widening (dspread>0) raises surrenders."""
    return q0 * math.exp(gamma * max(0.0, dspread_bps) / 10000.0)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--q0", type=float, required=True, help="base lapse rate, e.g. 3.1 (pct, [O])")
    ap.add_argument("--dspread-bps", type=float, required=True, help="lagged spread widening, bps")
    ap.add_argument("--surrender-base", type=float, default=None, help="optional base surrender volume (EUR m) [O]")
    args = ap.parse_args()
    for name, g in GAMMA_BAND.items():
        q = project_lapse(args.q0, args.dspread_bps, g)
        line = f"{name:8s} gamma={g:5.1f}  q_t={q:6.2f}%  multiplier=x{q/args.q0:5.2f}"
        if args.surrender_base:
            line += f"  volume={args.surrender_base * q / args.q0:10.1f} mln"
        print(line)


if __name__ == "__main__":
    main()

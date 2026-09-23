#!/usr/bin/env python3
"""
05_viz_rfr.py — Figure per la tesi dai dati [O] (nessun input non verificato).

Output: reports/figures/*.png
  fig1_term_structures.png  — curve EIOPA EUR no_VA, 4 date (linee)
  fig2_va_evolution.png     — VA per data: 3 -> 14 -> 17 -> 19 bps (barre)
  fig3_repricing.png        — shifts vs 31/12/2021 per scadenza (barre raggruppate)
  fig4_duration_dphb.png    — duration implicita 2021 vs 2022 dal VA (barre)

Dipendenze: polars, matplotlib (gia' in requirements per l'app).
"""
from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import polars as pl

REPO = Path(__file__).resolve().parents[1]
CURVES = REPO / "data" / "processed" / "rfr_curves_eur_2021_2022.csv"
OUT = REPO / "reports" / "figures"
OUT.mkdir(parents=True, exist_ok=True)

DATES = ["2021-12-31", "2022-05-31", "2022-09-30", "2022-12-31"]
COLORS = ["#2563eb", "#0891b2", "#ea580c", "#16a34a"]
plt.rcParams.update({"figure.dpi": 150, "font.size": 9})


def main() -> None:
    df = pl.read_csv(CURVES).filter(pl.col("quality") == "verified")

    # fig1 — strutture a termine no_VA
    fig, ax = plt.subplots(figsize=(7, 4.2))
    for date, color in zip(DATES, COLORS):
        s = df.filter((pl.col("ref_date") == date) & (pl.col("sheet") == "no_VA")).sort("maturity")
        ax.plot(s["maturity"], s["rate"] * 100, marker="o", ms=3, color=color, label=date)
    ax.axhline(0, color="gray", lw=0.6, ls="--")
    ax.set(xlabel="Maturità (anni)", ylabel="Tasso spot (%)", title="Curve EIOPA RFR EUR (no VA) 2021-2022 [O]")
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(OUT / "fig1_term_structures.png")
    plt.close(fig)

    # fig2 — VA per data
    va = df.group_by("ref_date").agg(pl.col("va_bps").first()).sort("ref_date")
    fig, ax = plt.subplots(figsize=(5, 3.4))
    ax.bar(va["ref_date"], va["va_bps"], color=COLORS[-1], width=0.55)
    for x, v in zip(va["ref_date"], va["va_bps"]):
        ax.text(x, v + 0.4, f"{v} bps", ha="center", fontsize=9)
    ax.set(ylabel="VA (bps)", title="Volatility Adjustment EUR per data [O]\n(cross-validato: 19 bps = SFCR PVG 2022)")
    ax.set_ylim(0, 22)
    fig.tight_layout()
    fig.savefig(OUT / "fig2_va_evolution.png")
    plt.close(fig)

    # fig3 — shift per scadenza vs 31/12/2021
    piv = df.filter(pl.col("sheet") == "no_VA").pivot(on="ref_date", index="maturity", values="rate").sort("maturity")
    fig, ax = plt.subplots(figsize=(7, 4.2))
    w = 0.25
    mats = piv["maturity"]
    for i, date in enumerate(DATES[1:], start=1):
        shift = (piv[date] - piv["2021-12-31"]) * 10_000
        ax.bar(mats + (i - 2) * w, shift, width=w, color=COLORS[i], label=f"vs {date}")
    ax.set(xlabel="Maturità (anni)", ylabel="Shift (bps)", title="Shift reali della curva vs 31/12/2021 [O]")
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(OUT / "fig3_repricing.png")
    plt.close(fig)

    # fig4 — duration implicita dal VA: finding DPHB
    TP = {"2021-12-31": 151_694_417, "2022-12-31": 133_029_385}
    IMP = {"2021-12-31": 217_453, "2022-12-31": 565_931}
    fig, ax = plt.subplots(figsize=(5, 3.4))
    dvals = []
    for date in TP:
        va_bps = int(df.filter(pl.col("ref_date") == date)["va_bps"][0])
        dvals.append(IMP[date] / (TP[date] * va_bps / 10_000))
    ax.bar(list(TP), dvals, color=["#2563eb", "#ea580c"], width=0.45)
    for x, v in zip(TP, dvals):
        ax.text(x, v + 0.08, f"{v:.2f}", ha="center", fontsize=10)
    ax.set(ylabel="Duration implicita", title="Duration implicita dal VA [E-derived]\n2021: lineare ok — 2022: assorbimento DPHB")
    fig.tight_layout()
    fig.savefig(OUT / "fig4_duration_dphb.png")
    plt.close(fig)

    print(f"OK: 4 figure in {OUT}")


if __name__ == "__main__":
    main()

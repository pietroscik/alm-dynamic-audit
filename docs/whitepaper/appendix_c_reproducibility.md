# Appendice C — Riproducibilità

## C.1 Pipeline

    data/raw (SFCR/EIOPA, libreria documentale)
      → data/interim (CSV tracciati + SOURCES_addendum_*.md)
      → data/processed (curve, backtest)
      → models/ (parametri [E-model])
      → notebooks/01-09 (analisi riproducibili)
      → docs/whitepaper/

## C.2 Scripts

- scripts/integrate_rfr_macro.py — integra curve+macro (dry-run di default; --apply per scrivere)
- scripts/verify_dataset.py — invarianti QA, exit≠0 al fallimento
- scripts/dynamic_engine.py — motore lapse: q_t = q0·exp(γ·max(0, Δs_{t-1})), banda [19.7, 30.1], lag 1
- notebooks/04-09 — repricing RFR, viz, pannelli, proiezione 2021-2026

## C.3 Comandi di verifica (ambiente locale)

    python scripts/integrate_rfr_macro.py        # dry-run
    python scripts/integrate_rfr_macro.py --apply
    python scripts/dynamic_engine.py --q0 3.5 --dspread-bps 76
    python notebooks/09_projection_2023_2026.py  # genera il CSV del backtest
    pytest tests/                                # incl. test_rfr_curves.py
    python scripts/verify_dataset.py

## C.4 Principi

1. Nessun dato [O] privo di (documento, sezione).
2. Nessuna scrittura a file di dati senza dry-run esplicito.
3. Nessuna interpolazione di n.d. (proiezioni a floor dichiarate come [E-model]).
4. Ogni commit che aggiunge dati estende l'Appendice B.

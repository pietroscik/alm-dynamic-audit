# INTEGRITY_REPORT — Snapshot (2026-09-23, post-consolidamento)

Head al momento dello snapshot: commit di consolidamento (LICENSE, README, CI,
verify_new_datasets, Appendice D §D.2 MET-1..7, KNOWN_GAPS aggiornato).

## 1. Struttura (verificata via GitHub API, refs/heads/main)

- data/interim: 19 file (7 SOURCES addendum + closure + CSV panel/lapse/asset mix). ✔
- data/processed: 8 file (curve 2021-22 e 2023-26, backtest, macro, BACKTEST md). ✔
- data/raw: vuoto per design (nessun documento sorgente committato: copyright). ✔
- models: 3 (lapse params, stima γ, stabilità γ). ✔
- scripts: 4 (integrate_rfr_macro, verify_dataset, verify_new_datasets, dynamic_engine). ✔
- src: 12 moduli engine (non ispezionabili via API: contenuto locale). —
- app: app.py (Streamlit). —
- notebooks: 11 (01-09 + 2 md). ✔
- docs/whitepaper: 13 documenti (exec summary, outline, ch.1-7, app.A-D, INTEGRITY). ✔
- tests: 4. ✔
- root: LICENSE (MIT), README (v2), KNOWN_GAPS.md, data_dictionary + addendum,
  pyproject, requirements, modelspec. ✔

## 2. Catena commit

16 commit di contenuto dati/documenti tracciati in Appendice B (616c60f → questo commit);
commit infrastrutturali pregressi (fef609a…7aec972) annotati in Appendice B senza fonte
(nessun contenuto dati). CI attiva su push/PR: verify_dataset + verify_new_datasets + pytest.

## 3. Gate residui pre-rilascio (tutti locali)

1. Decisione dual-engine (scripts/ vs src/) e allineamento app/app.py alla specificazione
   validata (γ band [19,7; 30,1], lag-1, floor).
2. Merge data_dictionary addendum → data_dictionary.csv.
3. CI verde + pytest locale + verify exit 0.
4. Tag v1.0 + release (dopo 1-3).

## 4. Verdetto

Repository integro nella forma (post-consolidamento) e nella sostanza (tesi supportata
da 16 commit tracciati, limitazioni MET dichiarate come perimetro). Difficabile da
contestare su dati; residualmente esposto solo sul piano dell'implementazione locale
(dual-engine), in chiusura con il gate 1.

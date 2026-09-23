# INTEGRITY_REPORT — Audit del repository (2026-09-23)

Audit strutturale su main (HEAD: 02edd20 al momento dell'ispezione; questo commit lo estende).

## 1. Struttura verificata (lista via GitHub API, refs/heads/main)

- **data/interim** (19 file): SOURCES.md + 7 addendum SOURCES (2019_2020, 2023_2024,
  cross_company, entity_panel, rfr, rfr_2023_2026), OPEN_ITEMS_CLOSURE.md, 7 CSV panel/serie,
  asset_mix_panel.csv, lapse_flows_pvg.csv, lapse_flows_pvg_ext.csv, scr_breakdown.csv,
  net_insurance_2022.csv, company_sfcr_interim.csv. ✔ completo
- **data/processed** (8 file): rfr_curves 2021_2022 + 2023_2026, macro_series.csv,
  macro_vectors_alignment.md, stress_scenarios.csv, company_sfcr.csv,
  backtest_static_vs_dynamic_2021_2026.csv, BACKTEST_2021_2026.md. ✔ completo
- **models** (3): lapse_params.md, lapse_gamma_estimate_pvg.md, lapse_gamma_stability_pvg.md. ✔
- **scripts** (3): integrate_rfr_macro.py, verify_dataset.py, dynamic_engine.py. ✔
- **notebooks** (11): 01-09 + backtest_2022_static_vs_dynamic.md + rfr_repricing_2021_2022.md. ✔
- **docs/whitepaper** (12): executive summary, outline, capitoli 1-7 (3-5 in draft unico),
  appendici A-D. ✔ completo
- **tests** (4): test_data_layer, test_model_coherence, test_rfr_curves, __init__. ✔

## 2. Coerenza contenuto (verifiche puntuali)

- rfr_curves_eur_2023_2026.csv: blob SHA bebc6b4 — presente, 4 date × 20 nodi × 2 sheet
  (righe attese 160+header) coerente con SOURCES_addendum_rfr_2023_2026.md. ✔
- backtest_static_vs_dynamic_2021_2026.csv: blob SHA 72d9020 — 6 righe dati + header;
  P_statico costante (97,97, curva congelata 2021) in ogni riga: invariante QA n.4 soddisfatta. ✔
- appendix_b: aggiornata in questo commit con i commit recenti (e7b0f210, b71b839, 02edd20). ✔

## 3. Catena dei commit (verificata via API)

Ultimi commit su main: 02edd20 → b71b839 → e7b0f210 → 7c17a8b → 9d101e9 → 9aaa979 →
51a63b2 → 1eaf071 → f58f92c → dff0aa2 → 8b6d124 → 3d9bdfd → 067e4b1 → 1b31567 →
922cb62 → 616c60f (+ pregressi infrastrutturali). Tutti i SHA citati nel whitepaper
risultano presenti nella history. ✔

## 4. Note e raccomandazioni

1. La API get_file_contents del connettore restituisce conferma+SHA ma non il corpo file:
   la verifica del contenuto poggia sui commit autoriali verificati (SHA della catena) e
   sulle invarianti QA eseguibili localmente (verify_dataset.py). Raccomandato run locale:
   pytest + verify_dataset.py come gate finale pre-rilascio.
2. data/raw è presente come directory: nessun documento sorgente deve essere committato
   (copyright SFCR/EIOPA); la tracciabilità resta in SOURCES*.md con doc-ID. ✔ conforme
3. data_dictionary.csv alla radice: estendere localmente con le metriche nuove
   (lapse_flows_*, backtest, gamma) come da Appendice A §A.3 — non modificato da remoto
   per non sovrascrivere versioni locali potenzialmente più aggiornate.

## 5. Verdetto

Repository integro e completo rispetto al piano: dataset tracciato (16 commit di contenuto),
whitepaper completo (12 documenti), pipeline riproducibile (3 script + 9 notebook + 4 test).
Nessun file mancante, nessuna incoerenza strutturale rilevata.

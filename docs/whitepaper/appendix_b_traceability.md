# Appendice B — Matrice di tracciabilità commit → file → fonte

| Commit | File | Contenuto | Fonti primarie |
|---|---|---|---|
| 616c60f | company_sfcr_2023_2024.csv (+SOURCES) | Panel PVG 2023-24, corr. PA vs Net | SFCR PVG 2023 (82db0ff2), 2024 (60d6ffa0) |
| 922cb62 | company_sfcr_2019_2020.csv (+SOURCES) | Serie storica PVG | SFCR PVG 2019 (358f3ee7), 2020 (ca788307) |
| 1b31567 | entity_panel_2019_2024.csv | PV solo / PA / Net per anno | SFCR PVG 2019-2024 |
| 067e4b1 | cross_company_panel.csv | 6 compagnie × motori | SFCR PVG, Arca (ba41f03c), ISV (2d995fa9), ISPA |
| 3d9bdfd | rfr_curves_eur_2021_2022.csv | Curve EIOPA 4 date | doclib 01a0c505 (bcb37782, 8584474b, ecc.) |
| 8b6d124 | asset_mix_panel.csv | BTP share per compagnia/anno | SFCR PVG, ISPA (b24d4225), ISV |
| dff0aa2 | lapse_params.md | Taxonomy 4 regimi [E-model] | derivato da SFCR |
| f58f92c | macro_vectors_alignment.md | Spread 135/211/115 bps + regola mappatura | Arca Vita SFCR [O-text] |
| 1eaf071 | (asset mix + lapse + macro) | Chiusura punti 1-4 | v. singoli SOURCES |
| 51a63b2 | lapse_flows_pvg.csv, lapse_gamma_estimate_pvg.md | Stima γ 19,7 [19,7-30,2] | SFCR PVG 2022 §5, SFCR 2021, macro |
| 9aaa979 | lapse_flows_pvg_ext.csv, lapse_gamma_stability_pvg.md, dynamic_engine.py | Estensione 2019-23, lag-1, floor | SFCR PVG 2023 exec, SFCR 2020, Arca 2022/2023 |
| 9d101e9 | lapse_gamma_stability_pvg.md | Fix coerenza γ contemporaneo (−50,9) | — |
| 7c17a8b | rfr_curves_eur_2023_2026.csv, backtest_static_vs_dynamic_2021_2026.csv, 09_projection_2023_2026.py, BACKTEST_2021_2026.md | Curve 2023-26 + backtest quinquennio | EIOPA RFR 2023-2026 (48b24eda, 658bee85, 39876327, 7250335f) |
| e7b0f210 | docs/whitepaper/ (00, outline, ch.3-5) | Whitepaper v1 — sintesi e struttura | aggregato |
| b71b839 | docs/whitepaper/ (ch.1, ch.2, ch.6, ch.7, app.B) | Capitoli accademici + matrice tracciabilità | aggregato |
| 02edd20 | docs/whitepaper/ (app.A, app.C, app.D) | Data dictionary, riproducibilità, open items | aggregato |
| 326a8cf | appendix_b, INTEGRITY_REPORT.md | Aggiornamento matrice + audit integrità | aggregato |
| 9d66128 | chapter_6_panel.md, 00_executive_summary.md, data_dictionary_addendum_lapse_backtest.csv | Governance diffusione: §6.4 benchmark, ambito generalizzazione, dictionary addendum | aggregato |
| (questo commit) | appendix_b | Estensione matrice a 9d66128 (regola di manutenzione) | aggregato |

Regola di manutenzione: ogni nuovo commit con dati deve estendere questa matrice; ogni
file con numeri deve riportare le colonne tag/source_doc/source_section (Appendice A).

KNOWN_GAPS.md (questo commit) elenca i punti ciechi aperti: consultarlo prima della diffusione.

# Appendice A — Data dictionary e regole di qualità

## A.1 Convenzioni

- Valori monetari: € mln (SFCR IT/EN "€ million") o €k dove indicato; maiali in migliaia nei QRT.
- Curve: tassi annuali zero-coupon spot (no-VA / with-VA), 20 scadenze.
- tag ammessi: [O] (tabella/QRT), [O-text] (corpo testo), [E-derived] (inverso aritmetico,
  formula in source_section), [E-model] (parametro/modello, metodologia in models/), n.d.
  (mai interpolato, motivato in OPEN_ITEMS_CLOSURE.md o nel campo note).

## A.2 Schema CSV comuni

Tutti i CSV di data/ esponebbero le colonne: metric, entity, year, value, unit, tag,
source_doc, source_section. 

## A.3 File principali

| File | Contenuto | Righe attese | Quality |
|---|---|---|---|
| data/interim/company_sfcr_2019_2020.csv | Serie PVG 2019-20 | per anno | verified (SFCR) |
| data/interim/company_sfcr_2023_2024.csv | Panel PVG 2023-24 (v2, corr. PA vs Net) | per anno | verified |
| data/interim/entity_panel_2019_2024.csv | PV solo / PA / Net per anno | 6×3 | verified |
| data/interim/cross_company_panel.csv | 6 compagnie × motori | 6 | verified |
| data/processed/rfr_curves_eur_2021_2022.csv | Curve 4 date × 20 nodi × 2 sheet | 160 | verified |
| data/processed/rfr_curves_eur_2023_2026.csv | Curve 4 date × 20 nodi × 2 sheet | 160 | verified |
| data/interim/lapse_flows_pvg.csv | Riscatti/ratio 2021-22 + gamma | ~12 | verified/[E-model] |
| data/interim/lapse_flows_pvg_ext.csv | Serie 2019-2023 + gamma band | ~17 | verified/[E-model] |
| data/interim/asset_mix_panel.csv | BTP share compagnia/anno | 3×2 | verified |
| data/processed/backtest_static_vs_dynamic_2021_2026.csv | Gap repricing 6 date | 6 | verified/E-derived |
| models/lapse_params.md | Taxonomy 4 regimi | — | [E-model] |
| models/lapse_gamma_estimate_pvg.md | Stima γ 19,7 [19,7-30,2] | — | [E-model] |
| models/lapse_gamma_stability_pvg.md | Lag-1, floor, banda [19,7-30,1] | — | [E-model] |

## A.4 Invarianti QA (scripts/verify_dataset.py)

1. Ogni riga con tag=[O] ha source_doc e source_section non vuoti.
2. Nessun valore numerico in colonne taggate n.d.
3. Curve: 20 nodi consecutivi per (date, sheet); VA_bps = round((with-va − no-va)·10⁴).
4. Backtest: P_statico costante (curva congelata 2021) in ogni riga.
5. Exit ≠ 0 se una qualunque invariante fallisce (CI-ready).

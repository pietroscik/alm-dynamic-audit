# Appendice D — Open items e n.d. documentati

## D.1 Dati non disponibili (n.d.)

| Item | Dato | Stato | Motivazione |
|---|---|---|---|
| OCR-1 | Ratio ISV 2020, 2021 | n.d. definitivo | OCR corrotto ("2095"); nessuna inferenza su celle non verificabili |
| RES-1 | Residuo PV_SOLO 2022 (−6.065k) | annotato | componente "TP as-a-whole", nessuna ripartizione inventata |
| SRC-1 | Spread BTP-Bund 2024, 2025, 2026 | n.d. | nessuna fonte [O] nel corpus; motore lapse applica floor (proiezione d'isteresi dichiarata [E-model]) |
| CURVE-1 | Curve EIOPA 2025/2026 metadati | risolto | summary errata ("2021-11-15"); data verificata nel Main_Menu (31-01-2025, 31-01-2026), see SOURCES_addendum_rfr_2023_2026.md |
| VA-1 | Anomalia VA 2021 (217 mln impatto, minimo storico) | documentato | coerente con VA 3 bps; nessuna rettifica |
| SCR-1 | SCR lapse PVG 2022 | n.d. | non leggibile dai QRT OCR del SFCR 2022; serie SCR lapse disponibile 2020-21 [O] |

## D.2 Limitazioni metodologiche dichiarate (perimetro di validita')

Queste non sono n.d.: sono scelte metodologiche il cui effetto e' direzionale e dichiarato.
Chi le contesta contesta il perimetro, non i risultati: la direzione dei gap non dipende da esse.

| Item | Limitazione | Effetto dichiarato |
|---|---|---|
| MET-1 | Misure lapse non omogenee: 2021-22 su riserve aperture (3,1/3,6), 2022-23 su riserve medie (3,5/4,4) | La validazione lag-1 (γ=30,1) usa la serie a riserve medie; il confronto con la banda stimata su aperture e' indicativo, non identico per costruzione |
| MET-2 | "Lapses" 2023 (IFRS17, include riduzioni/riscatti parziali) vs "surrenders" 2022 (settlement) | Il confronto di volumi 2022-2023 (6.945 [E-derived]) e' un upper bound approssimato; le frequenze (3,5→4,4%) sono invece omogenee intra-SFCR 2023 |
| MET-3 | Rilevazioni miste nel backtest: 31.12 (2021-22) e 31.01 (2023-26) | Distanza di un mese: non influenza la direzione del gap; dichiarata per trasparenza |
| MET-4 | Repricing su curve no-VA mentre gli SFCR valutano TP con VA | Confronto internamente coerente (stessa base no-VA); il gap −18,6/−24,2 e' da intendersi in termini no-VA |
| MET-5 | Portafoglio teorico 10y a duration costante | Bound superiore; la duration implicita PVG (4,78→2,24) e' essa stessa endogena (state-dependence) |
| MET-6 | γ stimato su 2-3 osservazioni annue | Calibrazione puntuale; la banda [19,7; 30,1] e' uno stress triangolare, non un intervallo di confidenza statistico |
| MET-7 | Proxy BTP-Bund per la variabile interna PVG ("spread + rendimento retrocesso GS") | Conservativa in direzione: il legame con la GS attenua la sensitivita' |

Regola: un n.d. si riapre solo con una nuova fonte [O], mai con un'inferenza. Una
limitazione MET si promuove a n.d. solo se emerge che invalida la direzione del risultato.

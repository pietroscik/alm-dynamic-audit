# SOURCES — Addendum: Poste Vita Group 2023 e 2024

CORREZIONE (v2): nel documento precedente i dati EOF 371.389 / SCR 158.321 / ratio 234,58% /
MCR 65.193 erano attribuiti a Net Insurance: sono di **POSTE ASSICURA** (E.1.1 SFCR 2023).
Net Insurance S.p.A. 2023: EOF 47.909, SCR 20.357, MCR 5.089, ratio 235,34%.
SCR PA 2024 = 186.766 (non 186.800). Il panel completo per entita' e in
entity_panel_2019_2024.csv + SOURCES_addendum_entity_panel.md.

Estensione del panel oltre il periodo di backtest (2021-2022). Tutti i valori [O] in EUR migliaia (€k),
tracciati a (documento, sezione/QRT). Documenti: SFCR unico Poste Vita Group 31/12/2023 (EN, doc library
alm-dynamic, id 82db0ff2-0ad5-4c2b-bc79-0132efd27a83) e SFCR unico 31/12/2024 (EN, id
60d6ffa0-bdec-49f9-943a-a2c319201c06).

## PV_GROUP 2023
| Metrica | Valore (€k) | Fonte |
|---|---|---|
| BEL | 141.463.778 | SFCR 2023, D.2 tabella TP nette (life 140.965.914 + non-life 497.864) |
| Risk Margin | 4.278.043 | SFCR 2023, D.2 (life 4.257.307 + non-life 20.735) |
| TP lordo | 145.741.821 | SFCR 2023, D.2 |
| TP netto | 145.496.901 | SFCR 2023, D.2 (recuperi 244.920) |
| TMTP | 0 | SFCR 2023, p.119 |
| EOF SCR | 14.098.823 | SFCR 2023, S.22.01.21 (Tier I 12.079.749; Tier II 2.019.074) |
| SCR gruppo | 4.591.654 | SFCR 2023, S.23.01 R0680 |
| Ratio | 307,05% | SFCR 2023, S.23.01 R0690 |
| MCR gruppo | 2.066.245 | SFCR 2023, E.2 coverage table |
| Excess of assets over liabilities | 12.093.900 | SFCR 2023, S.23.01 R0700 |
| Attivi totali | 165.107.921 | SFCR 2023, S.02.01.02 R0500 (p.170); cash R0410 3.790.519 |
| Investimenti (R0070) | 143.744.832 | SFCR 2023, S.02.01.02 R0070 |
| Investments finanziari totali | 155.900.209 | SFCR 2023, tabella Financial Investments; govt bond 88.535.811 |
| VA: impatto su TP / EOF | +571.199 / −393.674 | SFCR 2023, S.22.01.21 |

## PV_GROUP 2024
| Metrica | Valore (€k) | Fonte |
|---|---|---|
| BEL | 148.744.706 | SFCR 2024, D.2 (life 148.154.733 + non-life 589.973) |
| Risk Margin | 3.574.559 | SFCR 2024, D.2 (life 3.544.291 + non-life 30.268) |
| TP lordo | 152.319.265 | SFCR 2024, D.2 |
| TP netto | 152.039.107 | SFCR 2024, D.2 (recuperi 280.157) |
| TMTP | 0 | SFCR 2024 |
| EOF SCR | 13.920.129 | SFCR 2024, S.23.01 R0660 (T1UR 11.120.171; T1R 778.308; T2 2.021.650); EOF MCR 12.170.129 |
| SCR gruppo | 4.314.983 | SFCR 2024, S.23.01 R0680 |
| Ratio | 322,60% | SFCR 2024, S.23.01 R0690 |
| MCR gruppo | 1.941.742 | SFCR 2024, E.2 coverage table |
| Excess of assets over liabilities | 12.650.497 | SFCR 2024, S.23.01 R0700 |
| Attivi totali | 171.781.131 | SFCR 2024, S.02.01.02 R0500 (p.114); cash R0410 4.690.070 |
| Government bonds | 90.338.926 | SFCR 2024, tabella Financial Investments |
| VA: impatto su TP / EOF / SCR | +572.475 / −393.517 / +24.043 | SFCR 2024, S.22.01.22 (p.117) |

## Per entita' (dettaglio in entity_panel_2019_2024.csv)
- Poste Vita solo 2023: EOF 14.079.290, SCR 4.532.196, MCR 2.039.488, ratio 310,65% / 604,53%
- Poste Vita solo 2024: EOF 13.899.090, SCR 4.171.784, MCR 1.877.303, ratio 333,17% / 647,16%
- Poste Assicura 2023: EOF 371.389, SCR 158.321, MCR 65.193, ratio 234,58%; IVASS procedimento
  add-on (lettera 6/3/2024)
- Poste Assicura 2024: EOF 438.856, SCR 186.766, MCR 70.127, ratio 234,98% / 625,80%
- Net Insurance spa 2023: EOF 47.909, SCR 20.357, MCR 5.089, ratio 235,34%
- Net Insurance spa 2024: EOF 60.172, ratio 229,54%
- Net Insurance Life 2023: EOF 101.628, SCR 50.345, MCR 18.735; 2024: ratio 230% (testo)

## Coerenza incrociata
- EOF gruppo 2023 14.098.823 = testo 2024 "EUR 14.099 mln" ✓
- SCR 2023 4.591.654 = "EUR 4.592 mln" ✓; SCR 2024 4.314.983 = "EUR 4.315 mln" ✓
- Ratio 307,05% → 322,60% = "dal 307% al 323%" ✓
- VA impatto TP 2022 (565.931) ~ 2023 (571.199) ~ 2024 (572.475): VA ~19bps stabile ✓
- TMTP = 0 confermato per 2023 e 2024 ✓
- PV solo 2022 EOF 12.804.895 = KPI comparativo SFCR 2023 ✓ = gruppo (AOF a livello solo) ✓

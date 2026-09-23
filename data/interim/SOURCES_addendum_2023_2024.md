# SOURCES — Addendum: Poste Vita Group 2023 e 2024

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
| TMTP | 0 | SFCR 2023, p.119: "il valore della misura transitoria al 31.12.2023 è 0" |
| EOF SCR | 14.098.823 | SFCR 2023, S.22.01.21 (Tier I 12.079.749; Tier II 2.019.074) |
| SCR gruppo | 4.591.654 | SFCR 2023, S.23.01 R0680 |
| Ratio | 307,05% | SFCR 2023, S.23.01 R0690 (coerente con testo "dal 253% al 307%") |
| Excess of assets over liabilities | 12.093.900 | SFCR 2023, S.23.01 R0700 |
| Attivi totali | 165.107.921 | SFCR 2023, S.02.01.02 R0500 (p.170); cash R0410 3.790.519 |
| Investimenti (R0070) | 143.744.832 | SFCR 2023, S.02.01.02 R0070 |
| Investments finanziari totali | 155.900.209 | SFCR 2023, tabella Financial Investments (31/12/2023); govt bond 88.535.811 |
| VA: impatto su TP / EOF | +571.199 / −393.674 | SFCR 2023, S.22.01.21 "Impact of volatility adjustment set to zero" |
| MCR gruppo | n.d. | Non individuato nelle sezioni estratte (MCR solo PV 2.039.488; PA 65.193; Net 18.735) |

Note: Poste Vita solo 2023: SCR 4.532.196 (da 4.967.417), MCR 2.039.488, ratio 310,65%, MCR ratio 604,53%
(E.2). Net Insurance 2023: EOF 371.389, SCR 158.321, ratio 234,58%.

## PV_GROUP 2024
| Metrica | Valore (€k) | Fonte |
|---|---|---|
| BEL | 148.744.706 | SFCR 2024, D.2 tabella TP nette (life 148.154.733 + non-life 589.973) |
| Risk Margin | 3.574.559 | SFCR 2024, D.2 (life 3.544.291 + non-life 30.268) |
| TP lordo | 152.319.265 | SFCR 2024, D.2 |
| TP netto | 152.039.107 | SFCR 2024, D.2 (recuperi 280.157) |
| TMTP | 0 | SFCR 2024: misura transitoria pari a 0 al 31.12.2024 |
| EOF SCR | 13.920.129 | SFCR 2024, S.23.01 R0660 (T1UR 11.120.171; T1R 778.308; T2 2.021.650); EOF MCR 12.170.129 |
| SCR gruppo | 4.314.983 | SFCR 2024, S.23.01 R0680 |
| Ratio | 322,60% | SFCR 2024, S.23.01 R0690 (coerente con testo "dal 307% al 323%") |
| Excess of assets over liabilities | 12.650.497 | SFCR 2024, S.23.01 R0700 |
| Attivi totali | 171.781.131 | SFCR 2024, S.02.01.02 R0500 (p.114); cash R0410 4.690.070 |
| Government bonds | 90.338.926 | SFCR 2024, tabella Financial Investments (31.12.2024); ~75% emittente italiano |
| Financial investments totali | 162.314.852 | SFCR 2024, somma componenti tabella (equities 370.047 + govt 90.338.926 + corporate 21.636.614 + structured 46.277 + CIU 32.948.891 + i/u 16.973.297 + deposits ~800) — voci Deposits parzialmente troncate: [E-derived somma] |
| VA: impatto su TP / EOF / SCR | +572.475 / −393.517 / +24.043 | SFCR 2024, S.22.01.22 (p.117) |
| MCR gruppo | n.d. | Non individuato nelle sezioni estratte |

Note 2024: Poste Assicura solo EOF 438.856, SCR 186.800, ratio 234,98%. Net Insurance solo EOF 60.172,
ratio 229,54%, MCR 23.614. PV solo 2024: assets 170.541.444 (S.02.01.02, p.123).

## Curve EIOPA RFR — stato
- Disponibili in libreria (doclib://01a0c505-f098-75f6-8869-3fce317127c9): 20200811 (pubblicazione speciale, inutile), 20221231 (estratta EUR no_VA/with_VA nodi 1-20; VA nodo2 19bps ✓ coerente con SFCR 2022), 20230131, 20230531, 20240131, 20240630, 20250131, 20250630, 20260131, 20260630.
- MANCANTI per il backtest: 31/12/2021, 30/06/2022, 30/09/2022. Scaricabili dall'archivio EIOPA:
  https://www.eiopa.europa.eu/tools-and-data/risk-free-interest-rate-term-structures/risk-free-rate-previous-releases-and-preparatory-phase_en
  (zip mensili "December 2021", "June 2022", "September 2022").

## Coerenza incrociata
- EOF gruppo 2023 14.098.823 = testo 2024 "€ 14.099 mln" ✓
- SCR 2023 4.591.654 = testo 2024 "€ 4.592 mln" ✓; SCR 2024 4.314.983 = "€ 4.315 mln" ✓
- Ratio 307,05% → 322,60% = testo "dal 307% al 323%" ✓
- VA impatto TP 2022 (565.931) ~ 2023 (571.199) ~ 2024 (572.475): coerente con VA ~19bps stabile ✓
- TMTP = 0 confermato per 2023 e 2024 (verifica quadriennale 2022 permanente) ✓

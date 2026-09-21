# Tracciabilita fonti — dati reali estratti (layer interim)

Regola di accettazione: un valore entra come [O] solo se tracciabile a (documento, sezione/QRT, pagina/riga).
Unita: migliaia di Euro (EUR k) salvo diversa indicazione. Solvency_ratio in decimale.

## 1. PV_GROUP 31/12/2021 — fonte primaria: Single SFCR Poste Vita Group 2021 (b60d9d3a)

| Campo | Valore (EUR k) | Fonte esatta |
|---|---|---|
| own_funds (EOF eligible SCR) | 12,676,835 | S.23.01.22 R0560 (T1UR 10,364,195; T1R 298,590; T2 2,014,050; BOF R0290 10,926,835 + ancillary R0400 1,750,000) |
| scr | 4,441,175 | Sez. E.2, tabella SCR p.161 ("Solvency capital requirement") |
| mcr | 2,029,162 | S.23.01.22 R0610 (Minimum consolidated group SCR) |
| solvency_ratio | 285.4% | 12,676,835 / 4,441,175 |
| tp_total (con LTG/TMTP) | 151,694,417 | S.22.01.22 (Technical provisions, amount with LTG measures and transitionals) |
| bel (presentazione gruppo) | 151,468,375 | D.2 tabella "Net Technical Provisions" (Vita 151,234,448 + Danni 233,927) |
| risk_margin (presentazione gruppo) | 226,042 | D.2 medesima tabella (Vita 204,282 + Danni 21,760) |
| tmtp | 1,590,076 | S.22.01.22 "Impact of transitional on technical provisions" |
| total_assets | 168,333,019 | S.02.01.02 R0500 (p.167) |
| investments | 150,845,818 | S.02.01.02 R0070 |
| govt_bonds | 92,248,174 | S.02.01.02 R0140 |
| corporate_bonds | 23,075,784 | S.02.01.02 R0150 |
| structured_notes | 572,519 | S.02.01.02 R0160 |
| ciu | 34,832,715 | S.02.01.02 R0180 |
| equities | 7,777 | S.02.01.02 R0100 |
| ul_assets | 7,600,372 | S.02.01.02 R0220 |
| cash | 4,986,608 | S.02.01.02 R0410 (p.167); dettaglio D.1 p.~107 (solo PV 4,948,238) |
| excess_assets | 10,761,534 | S.02.01.02 R1000 |
| TP life excl UL | 144,105,252 | S.02.01.02 R0600 (p.168) |
| TP index/unit-linked | 7,333,477 | S.02.01.02 R0690 |
| TP non-life | 255,687 | S.02.01.02 R0510 |

Note metodologiche 2021:
- La compagnia usa TMTP (art. 308c / art. 344-decies CAP) con riduzione 62.50%; il TP riportato (151,694,417) e NETTO della deduzione transitoria. Decomposizione solo-entity PRE-TMTP: BEL lordo 151,718,144 + RM 1,310,662 - rec. 11,381 = TP netto 153,017,425; meno TMTP 1,590,076 = 151,427,349 (D.2 p.117).
- La tabella "Gestione Vita/Danni" di gruppo (BEL 151,468,375; RM 226,042) somma esattamente al TP con LTG: e una presentazione post-TMTP.
- VA: S.22.01.22 mostra impatto VA=0 su TP pari a 217,453 e su EOF 150,368 → la compagnia usa il Volatility Adjustment.
- Governo bond quota su investments: 92,248,174/150,845,818 = 61.2% (tutti i titoli di Stato, non solo BTP).

## 2. PV_GROUP 31/12/2022 — fonti: SFCR 2023 (comparativi) + Annual Report 2022 (54ddfa37)

| Campo | Valore (EUR k) | Fonte esatta |
|---|---|---|
| own_funds | 12,804,895 | SFCR 2023 KPI comparative (sez. A) + Annual Report 2022 p.33 (T1UR 10,064,015; T1R 727,630; T2 2,013,250) |
| scr | 5,055,992 | SFCR 2023 KPI comparative |
| mcr | 2,290,855 | SFCR 2023 KPI comparative |
| solvency_ratio | 253.26% | SFCR 2023 KPI comparative |
| govt_bonds | 79,576,592 | SFCR 2023 sez. A.3 tabella comparativa investimenti (valore 31/12/2022) |
| corporate_bonds | 20,248,782 | idem |
| ciu | 31,621,867 | idem |
| equities | 103,666 | idem |
| structured_notes | 545,310 | idem |
| ul_assets | 9,608,163 | idem |
| investments (finanziari) | 141,704,381 | idem (totale riga) |

MANCA per il 2022 (da reperire sul vero SFCR 2022 di Poste Vita Group, NON presente in libreria):
- BEL e Risk Margin Solvency II (sezione D.2)
- TMTP 2022
- S.02.01.02: total_assets, cash, excess of assets over liabilities
ATTENZIONE: il file "singlesolvencyfinancialconditionreport-postevitagroup-31122022.pdf" presente in libreria e in realta il BILANCIO CONSOLIDATO 2022, non l'SFCR. L'SFCR 2022 va scaricato dal sito Poste Vita (Societa Trasparente).

## 3. Poste Vita SOLO entity
- 2021: S.02.01.02 solo p.175 (total assets 168,004,994; cash 4,948,238); D.1 p.108 (govt 91,802,630; corp 23,007,974; structured 547,424; CIU 32,975,472; UL 7,600,372)
- 2022: KPI da SFCR 2023 comparativi (EOF 12,804,895; SCR 4,967,417; MCR 2,235,338; ratio 257.78%)

## 4. Benchmark
- SQ_Own_Funds.xlsx: EIOPA Insurance Statistics — Own funds and SCR [S.23.01/Quarterly/Solo], aggregato EEA, 2016Q3-2025Q2, EUR m (R0500/R0510/R0540 breakdown tier/R0550/R0580/R0600 + ratios R0620/R0640). Uso: benchmark di mercato per SPS, NON dati compagnia.
- 20240605_ReportSFCR2023_Def.pdf: report CCA "La solvibilita delle Compagnie Assicurative italiane nel 2023" (top 20 per premi).
- 2026-report-insurance-market-performance-overview.pdf: report PwC mercato.

## 5. Serie macro
Le curve EIOPA RFR (31/12/2021, 30/06/2022, 30/09/2022, 30/12/2022) NON sono in libreria: scaricare gli zip da eiopa.europa.eu (RFR previous releases), fogli RFR_spot_no_VA / RFR_spot_with_VA, colonna EUR, nodi 1-20y. Spread BTP-Bund e inflazione ISTAT restano da reperire dalle fonti primarie. I valori macro attualmente in data/processed/macro_series.csv restano flag synthetic finche non sostituiti.

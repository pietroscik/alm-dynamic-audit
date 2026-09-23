# Tracciabilita fonti — dati reali estratti (layer interim)

Regola di accettazione: un valore entra come [O] solo se tracciabile a (documento, sezione/QRT, pagina/riga).
Unita: migliaia di Euro (EUR k) salvo diversa indicazione. Solvency_ratio in decimale.

## 1. PV_GROUP 31/12/2021 — fonte primaria: Single SFCR Poste Vita Group 2021 (b60d9d3a)

| Campo | Valore (EUR k) | Fonte esatta |
|---|---|---|
| own_funds (EOF eligible SCR) | 12,676,835 | S.23.01.22 R0560 (T1UR 10,364,195; T1R 298,590; T2 2,014,050; BOF R0290 10,926,835 + ancillary R0400 1,750,000) |
| scr | 4,441,175 | Sez. E.2, tabella SCR p.161 |
| mcr | 2,029,162 | S.23.01.22 R0610 |
| solvency_ratio | 285.4% | 12,676,835 / 4,441,175 |
| tp_total (con LTG/TMTP) | 151,694,417 | S.22.01.22 |
| bel (presentazione gruppo) | 151,468,375 | D.2 tabella "Net Technical Provisions" (Vita 151,234,448 + Danni 233,927) |
| risk_margin (presentazione gruppo) | 226,042 | D.2 (Vita 204,282 + Danni 21,760) |
| tmtp | 1,590,076 | S.22.01.22 "Impact of transitional on technical provisions" |
| total_assets | 168,333,019 | S.02.01.02 R0500 (p.167) |
| investments | 150,845,818 | S.02.01.02 R0070 |
| govt_bonds | 92,248,174 | S.02.01.02 R0140 |
| corporate_bonds | 23,075,784 | S.02.01.02 R0150 |
| structured_notes | 572,519 | S.02.01.02 R0160 |
| ciu | 34,832,715 | S.02.01.02 R0180 |
| equities | 7,777 | S.02.01.02 R0100 |
| ul_assets | 7,600,372 | S.02.01.02 R0220 |
| cash | 4,986,608 | S.02.01.02 R0410 |
| excess_assets | 10,761,534 | S.02.01.02 R1000 |

Note metodologiche 2021: TMTP (art. 344-decies CAP) con riduzione 62.50%; TP riportato NETTO della deduzione transitoria. VA: S.22.01.22 impatto VA=0 su TP 217,453 e su EOF 150,368 → Volatility Adjustment in uso.

## 2. PV_GROUP 31/12/2022 — fonte primaria: Relazione Unica SFCR PVG 2022 (upload: relazioneunicasolvibilita-condizionefinanziaria-31122022.pdf)

| Campo | Valore (EUR k) | Fonte esatta |
|---|---|---|
| bel | 128,350,704 | D.2 p.105 (Vita 128,082,365 + Danni 268,339) |
| risk_margin | 4,678,681 | D.2 p.105; tabella RM p.118 (2021: 226,042) |
| tp_total | 133,029,385 | D.2 p.105 |
| tmtp | 0 | D.2 p.107: verifica quadriennale MTRT, differenza negativa per ogni LoB |
| total_assets | 152,155,637 | S.02.01.02 R0500 p.152 |
| investments | 132,206,834 | S.02.01.02 R0070 |
| govt_bonds | 79,576,592 | R0140 |
| corporate_bonds | 20,248,782 | R0150 |
| structured_notes | 545,310 | R0160 |
| ciu | 31,621,867 | R0180 |
| equities | 103,666 | R0100 |
| ul_assets | 9,608,163 | R0220 |
| cash | 2,924,160 | R0410 |
| excess_assets | 10,514,015 | R1000 p.153 |
| own_funds | 12,804,895 | S.23.01.22 R0560 p.158 |
| scr | 5,055,992 | S.25.01.22 p.159 |
| mcr | 2,291,047 | S.25.01.22 (= PV 2,235,338 + PA 55,709) |
| VA | 19 bps | D.2 p.113; azzeramento VA: TP +565,931; EOF -391,511; SCR +135,944 (S.22.01.22 p.155) |

ATTENZIONE: il file "singlesolvencyfinancialconditionreport-postevitagroup-31122022.pdf" in libreria e il BILANCIO CONSOLIDATO 2022 (KPI di solvibilita a p.33 ma nessun BEL/RM). L'SFCR vero 2022 e la Relazione Unica italiana.

## 3. Poste Vita SOLO entity
- 2021: S.02.01.02 solo p.175 (total assets 168,004,994; cash 4,948,238); D.1 p.108 (govt 91,802,630; corp 23,007,974; structured 547,424; CIU 32,975,472; UL 7,600,372); TP pre-TMTP: BEL lordo 151,718,144 + RM 1,310,662 - rec 11,381 = 153,017,425; meno TMTP 1,590,076 = 151,427,349 (D.2 p.117)
- 2022: D.2 p.107 (BEL lordo 128,082,365; RM 4,651,605; TP netto 132,727,905; MTRT 0); S.12.01.02 p.164; KPI solo p.14 (SCR 4,967,417; MCR 2,235,338)

## 4. Gruppo Net Insurance 31/12/2022 (upload: Gruppo-Net-Insurance-Solvency-II-31.12.2022.pdf)
SFCR Gruppo Net Insurance (Net Insurance SpA + Net Insurance Life), revisione KPMG 11/05/2023, 193 pagine. NON e Poste Vita: e il gruppo acquisito da Poste nel 2023 (OPA estate 2022). Dati gruppo: EOF 91,156; SCR 52,112; ratio 174.92%; TP 310,854 (BEL 303,421 + RM 7,435); TMTP 0; VA applicato. Coerenza incrociata con comparativi SFCR PVG 2023 (Net 91,812/45,661; NIL 33,217/18,940): MATCH.

## 5. Benchmark
- SQ_Own_Funds.xlsx: EIOPA Insurance Statistics — Own funds and SCR [S.23.01/Quarterly/Solo], aggregato EEA, 2016Q3-2025Q2, EUR m. Benchmark di mercato per SPS, NON dati compagnia.
- 20240605_ReportSFCR2023_Def.pdf: report CCA top-20 (SCR medio 255%->268%, VA +12pp medio).
- 2026-report-insurance-market-performance-overview.pdf: report PwC mercato.

## 6. Verifiche integrita documenti (ricontrollo completo)
- 54ddfa37 = Bilancio Consolidato IFRS 2022 (zero grep di "risk margin"/"Best Estimate"/QRT). KPI solvibilita utilizzabili solo come conferma.
- a6572589 = Relazione Unica 2021 italiana: duplicato di b60d9d3a (stessa approvazione CDA 28/04/2022).
- 8c47bd3c = Relazione Unica 2020 italiana: duplicato di ca788307.
- SFCR 2023 (82db0ff2): QRT solo 2023; comparativi 2022 solo in tabelle narrative.
- Caveat: tabella narrativa D.1 2021 "Total assets 108,333,619" = perimetro aggregato ridotto; usare S.02.01.02 R0500 = 168,333,019.

## 7. CORREZIONE METODOLOGICA breakdown SCR
Due presentazioni NON confrontabili:
1. SFCR 2022 QRT (lordo pre-LAC TP): market 7,613,259; life UW 13,469,741; BSCR 17,184,931; LAC TP -11,299,794 (65.8% del BSCR); LAC DT -1,596,629; addon 92,405; SCR 5,055,992.
2. SFCR 2023 comparativa (netto post-LAC TP): market 2,253,884; life UW 4,750,934; BSCR 5,885,137; SCR 5,055,992.
Usare la (1) per il 2022. LAC TP enorme = partecipazione agli utili/DPHB: da dichiarare in modelspec.md.

## 8. Riconciliazioni verificate (dataset completo)
- EOF/SCR 2022 = 12,804,895/5,055,992 = 253.26% (KPI p.14) OK
- MCR = 2,235,338 + 55,709 = 2,291,047 OK
- D.2: BEL+RM = TP per Gruppo, solo e ogni LoB OK
- Asset side S.02.01.02 2022 = comparativi SFCR 2023 A.3 OK
- EOF tiering = Annual Report 2022 p.33 OK
- Bridge EOF 2021->2022: -247,519 (excess) + 428,240 (subordinati AT1) - 52,661 (residuo) = +128,060 OK

Il dataset PVG 2021-2022 e COMPLETO (BEL/RM/TMTP/VA/assets/cash/EOF/SCR/MCR, gruppo e solo-entity).

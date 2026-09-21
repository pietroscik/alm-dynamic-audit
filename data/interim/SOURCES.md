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
| TP life excl UL | 144,105,252 | S.02.01.02 R0600 (p.168) |
| TP index/unit-linked | 7,333,477 | S.02.01.02 R0690 |
| TP non-life | 255,687 | S.02.01.02 R0510 |

Note metodologiche 2021:
- TMTP (art. 344-decies CAP) con riduzione 62.50%; TP riportato NETTO della deduzione transitoria. Decomposizione solo-entity PRE-TMTP: BEL lordo 151,718,144 + RM 1,310,662 - rec. 11,381 = TP netto 153,017,425; meno TMTP 1,590,076 = 151,427,349 (D.2 p.117).
- La tabella "Gestione Vita/Danni" di gruppo (BEL 151,468,375; RM 226,042) somma esattamente al TP con LTG: presentazione post-TMTP.
- VA: S.22.01.22 mostra impatto VA=0 su TP pari a 217,453 e su EOF 150,368 → la compagnia usa il Volatility Adjustment.
- Govt bonds / investments = 92,248,174/150,845,818 = 61.2% (tutti i titoli di Stato, non solo BTP).

## 2. PV_GROUP 31/12/2022 — fonti: SFCR 2023 (comparativi) + Annual Report 2022 (54ddfa37)

| Campo | Valore (EUR k) | Fonte esatta |
|---|---|---|
| own_funds | 12,804,895 | SFCR 2023 KPI comparative (sez. A) + Annual Report 2022 p.33 (T1UR 10,064,015; T1R 727,630; T2 2,013,250) |
| scr | 5,055,992 | SFCR 2023 KPI comparative |
| mcr | 2,290,855 | SFCR 2023 KPI comparative |
| solvency_ratio | 253.26% | SFCR 2023 KPI comparative |
| govt_bonds | 79,576,592 | SFCR 2023 sez. A.3 tabella comparativa (valore 31/12/2022) |
| corporate_bonds | 20,248,782 | idem |
| ciu | 31,621,867 | idem |
| equities | 103,666 | idem |
| structured_notes | 545,310 | idem |
| ul_assets | 9,608,163 | idem |
| investments (finanziari) | 141,704,381 | idem (totale riga) |

MANCA per il 2022 (da reperire sul vero SFCR 2022, NON presente in libreria):
- BEL e Risk Margin Solvency II (sezione D.2), TMTP 2022
- S.02.01.02: total_assets, cash, excess of assets over liabilities
ATTENZIONE: "singlesolvencyfinancialconditionreport-postevitagroup-31122022.pdf" in libreria e il BILANCIO CONSOLIDATO 2022, non l'SFCR.

## 3. Poste Vita SOLO entity
- 2021: S.02.01.02 solo p.175 (total assets 168,004,994; cash 4,948,238); D.1 p.108 (govt 91,802,630; corp 23,007,974; structured 547,424; CIU 32,975,472; UL 7,600,372)
- 2022: KPI da SFCR 2023 comparativi (EOF 12,804,895; SCR 4,967,417; MCR 2,235,338; ratio 257.78%)

## 4. Benchmark
- SQ_Own_Funds.xlsx: EIOPA Insurance Statistics — Own funds and SCR [S.23.01/Quarterly/Solo], aggregato EEA, 2016Q3-2025Q2, EUR m. Benchmark di mercato per SPS, NON dati compagnia.
- 20240605_ReportSFCR2023_Def.pdf: report CCA "La solvibilita delle Compagnie Assicurative italiane nel 2023" (top 20 per premi).
- 2026-report-insurance-market-performance-overview.pdf: report PwC mercato.

## 5. Serie macro
Curve EIOPA RFR NON in libreria: scaricare da eiopa.europa.eu (RFR previous releases) i file 31/12/2021, 30/06/2022, 30/09/2022, 30/12/2022, fogli RFR_spot_no_VA / RFR_spot_with_VA, colonna EUR. Spread BTP-Bund e inflazione ISTAT da fonti primarie. macro_series.csv resta flag synthetic finche non sostituito.

## 6. Riconsolidamento post-ricontrollo PDF (seconda passatura)

Verifiche effettuate su tutti i 29 documenti:
1. **54ddfa37 ("SFCR 2022")** = Bilancio Consolidato IFRS 2022. CONFERMATO: zero occorrenze di "risk margin", "Best Estimate", "Solvency II value", "Quantitative Reporting", "S.02.01", "Valuation for solvency". Nessun dato BEL/RM Solvency II 2022 estraibile da questo file.
2. **a6572589** = "Relazione Unica" 2021 in ITALIANO: duplicato tradotto dello SFCR 2021 inglese (b60d9d3a), stessa approvazione CDA 28/04/2022. Nessun dato nuovo.
3. **8c47bd3c** = "Relazione Unica" 2020 in ITALIANO: duplicato dello SFCR 2020 (ca788307).
4. **SFCR 2023 (82db0ff2)**: gli annex QRT riportano SOLO l'anno 2023; i comparativi 31/12/2022 esistono solo nelle tabelle narrative (sez. A KPI, A.3 investimenti, E.2 SCR). Nessun comparativo 2022 per TP/BEL/RM in sezione D.
5. **20240605_ReportSFCR2023_Def.pdf** = report CCA (benchmark top-20), non SFCR. **SQ_Own_Funds.xlsx** = EIOPA statistics EEA aggregato (EUR m), benchmark SPS.

### Dati dalla seconda passatura (SFCR 2023, tabella comparativa E.2) → data/interim/scr_breakdown.csv

**SCR Gruppo 31/12/2022 (EUR k)**: market 2,253,884; counterparty 300,286; life UW 4,750,934; health UW 113,797; non-life UW 40,176; diversification -1,573,938; **BSCR 5,885,137**; operational 675,079; SCR **5,055,992**. LAC DT non riportato esplicitamente: derivato = 5,885,137+675,079-5,055,992 = **-1,504,224** [E-derived].
**SCR Poste Vita solo 31/12/2022 (EUR k)**: market 2,300,953; counterparty 288,692; life UW 4,750,934; health 13,862; div -1,482,140; **BSCR 5,872,301**; op 663,774; LAC DT -1,569,658; **SCR 4,967,417**.
Nota coerente con 2021 (SFCR 2021 E.2): SCR solo 2021 ex add-on 4,396,571 + add-on 44,604 = 4,441,175 (Gruppo). Nel 2021 l'add-on era su Poste Assicura (IVASS); nel 2023 add-on PA 54,547 + proceeding IVASS 6/3/2024.

### Caveat sui totali attivi narrativi
La tabella narrativa D.1 2021 (p.~102) riporta "Total assets 108,333,619": NON usare - e una presentazione agregata ridotta (perimetro interno). Il riferimento corretto e il QRT S.02.01.02 R0500 = 168,333,019.

## 7. SFCR Gruppo Net Insurance 2022 (upload utente: Gruppo-Net-Insurance-Solvency-II-31.12.2022.pdf)

### IDENTIFICAZIONE
Relazione Unica SFCR del **Gruppo Net Insurance** (Net Insurance S.p.A. non-life + Net Insurance Life S.p.A.) al 31/12/2022, revisione KPMG 11/05/2023, 193 pagine, QRT di gruppo alle pp. 146-160.
ATTENZIONE: NON e l'SFCR Poste Vita Group 2022. Net Insurance e il gruppo acquisito da Poste Vita (operazione completata 2023) - e per questo che compare nell'SFCR PVG 2023 come controllata. Il gap BEL/RM Poste Vita 2022 resta APERTO.

### PERCHE E RILEVANTE PER LA TESI
1. Fornisce i dati reali Net Insurance/NIL al 31/12/2022 PRE-acquisizione: permette di riconciliare il cambio di perimetro tra SFCR PVG 2022 (assente) e SFCR PVG 2023 (include Net: EOF Net 91.812 + NIL 33.217 vs Gruppo Net consolidato 91.156 - la differenza e l'aggregazione metodo 1).
2. Coerenza incrociata verificata con SFCR PVG 2023 comparativi: Net Insurance EOF 91.812 / SCR 45.661 / ratio 201,07%; NIL EOF 33.217 / SCR 18.940 / ratio 175,35% → MATCH perfetto con tabella copertura p.129 dell'SFCR Net.
3. Caso di studio secondario: compagnia small-cap con VA applicato e TMTP = 0 (contrasto con PVG: TMTP 1,59 mld).

### DATI GRUPPO NET INSURANCE 31/12/2022 (EUR k)
- S.02.01.02 (p.147-148): total assets 501.425; investimenti 214.948 (govt 95.233; corp 43.953; CIU 70.998; equities 4.279); cash 6.795; total liabilities 417.739; eccedenza attivi 83.706
- TP (S.02.01.02): non-life 135.814 (BE 128.490 + RM 4.002; di cui health SLT 3.322 con BE 3.141 + RM 182); vita 175.513 (BE 172.306 + RM 3.208); health simile vita -673 (BE -516 + RM 43). BEL totale gruppo 303.421 + RM 7.435 = 310.854
- S.22.01.22 (p.150): TP con LTG 310.854; TMTP 0; impatto azzeramento VA: TP +1.609, EOF -716, SCR +674 → il gruppo usa il Volatility Adjustment (art. 77 quinquies), confermato anche a testo (p.28)
- EOF (p.129/150): ammissibili SCR 91.156 (T1 70.247; T2 13.092; T3 7.817); ratio 174,92%; MCR 21.500, ratio 346,73%
- S.25.01.22 (p.152): market 21.413; counterparty 10.411; life UW 14.688; health UW 5.185; non-life UW 30.848; diversificazione -28.895; BSCR 53.650; op risk 4.722; LAC DT -6.260; SCR 52.112
- Solvency ratio 2021 (comparativo p.129): Gruppo 181%, Net 201%

### Nota qualita OCR
Il PDF e stato processato via OCR: i numeri chiave sopra sono stati verificati per coerenza interna (BE+RM=TP per ogni LoB; BSCR+op-LACDT=SCR; EOF/SCR=ratio) e per coerenza esterna con gli stessi valori riportati nell'SFCR PVG 2023. La S.23.01.22 OCR e degradata: usare i totali da p.129.

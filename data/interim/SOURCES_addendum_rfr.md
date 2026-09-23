# SOURCES — Addendum: curve EIOPA RFR EUR 2021-2022

Tutti i valori [O]. Fonte: file EIOPA_RFR_<YYYYMMDD>_Term_Structures.xlsx in libreria
"Curve EIOPA Risk-Free Rate (RFR)" (doclib://01a0c505-f098-75f6-8869-3fce317127c9).
Fogli: RFR_spot_no_VA, RFR_spot_with_VA. Colonna: "Euro" (3ª colonna dati, riga di intestazione
nan,Main menu,Euro,...). Nodi 1-20 (LLP EUR = 20; UFR 3,6%; alpha 0,132807 al 31/12/2021).

| Data | File | doclib doc id |
|---|---|---|
| 31/12/2021 | EIOPA_RFR_20211231_Term_Structures.xlsx | bcb37782-1d49-4145-9830-c25462ef7158 |
| 31/05/2022 | EIOPA_RFR_20220531_Term_Structures.xlsx | daf05683-5451-4a68-ae6d-55a17678ed3a |
| 30/09/2022 | EIOPA_RFR_20220930_Term_Structures.xlsx | b06676fd-c282-47ae-9a2d-1b75a0769ec1 |
| 31/12/2022 | EIOPA_RFR_20221231_Term_Structures.xlsx | 8584474b-9b3f-4ecc-a8f5-5952d1468513 |

Note valori notevoli [O]:
- 31/12/2021 no_VA: n1 −0,585%, n2 −0,395%, n10 0,205%, n20 0,456%; with_VA: n1 −0,555%, n2 −0,365%
- 31/12/2022 no_VA: n1 3,176%, n2 3,295%, n10 3,092%, n20 2,765%; with_VA: n1 3,366%, n2 3,485%

Riconciliazioni:
- VA 31/12/2022 = 19 bps uniforme = VA dichiarato SFCR PVG 2022 (Relazione Unica, sezione D.2) ✓
- VA 31/12/2021 = 3 bps uniforme; impatto VA→0 su TP 217.453 (SFCR 2021, S.22.01.22) → duration implicita 4,78 ✓ coerente con D_L≈5,30 del notebook
- VA 31/12/2022: impatto 565.931 → duration implicita 2,24 (anomalia lineare → assorbimento DPHB, vedi notebook rfr_repricing)

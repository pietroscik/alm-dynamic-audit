# Vettori macro per anno — allineamento stress_scenarios [O]

## BTP-Bund 10y (fonte: SFCR Arca Vita, sezione andamenti di mercato [O-text])

| Data | BTP 10y | Bund 10y | Spread BTP-Bund |
|---|---|---|---|
| 31/12/2021 | ~3,31%* | ~1,96%* | **135 bps** (da 211 a fine 2022 meno +76 di aumento) |
| 31/12/2022 | 4,65% | 2,54% | **211 bps** (+76 su 2021) |
| 31/12/2024 | — | — | **115 bps** (da 168 inizio anno; BTP decennale "ottimo comportamento") |

*[E-derived] da 211−76=135; BTP/Bund fine 2021 ricavabili per differenza dai valori dichiarati 2022.
Fonte unica citabile: Relazione Arca Vita 2022 (C, andamenti di mercato) e 2024 (idem).

## Curve EIOPA RFR EUR disponibili in libreria (per anno di backtest)

| Ref date | File | Status |
|---|---|---|
| 31/12/2021 | EIOPA_RFR_20211231 | [O] estratta nodi 1-20 (rfr_curves_eur_2021_2022.csv) |
| 31/05/2022 | EIOPA_RFR_20220531 | [O] estratta |
| 30/09/2022 | EIOPA_RFR_20220930 | [O] estratta |
| 31/12/2022 | EIOPA_RFR_20221231 | [O] estratta, VA 19bps cross-validato |
| 31/01-31/05/2023 | EIOPA_RFR_2023*, 2024*, 2025* | in libreria, NON ancora estratte — estrarre con la stessa pipeline se il backtest si estende al 2023+ |

## Regola di mappatura per stress_scenarios (per anno a di ogni compagnia)
1. shock_tasso(a) = curva EIOPA 31/12/(a) − curva 31/12/(a−1), nodi 1-20 [O]
2. spread(a) = BTP-Bund dichiarato [O-text] dove disponibile, altrimenti [E] da dati di mercato
3. va(a) = VA EIOPA dichiarato in SFCR / cross-check con curva with_VA [O]
4. btp_impact(a) = btp_share(company, a) × spread_shock — SOLO se btp_share [O]; altrimenti stress uniforme con flag [E]

Il punto 4 e' la novita': con asset_mix_panel.csv lo shock spread non e' piu' uniforme.

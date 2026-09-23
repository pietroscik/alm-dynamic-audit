# Analisi backtest statico vs dinamico — PVG 2021→2022 (tutti i dati [O] salvo [E] indicato)

## 1. Motivi di calcolo: errore sul Solvency Ratio 2022 (effettivo: 253,26%)
| Motore | Ratio previsto | Errore (pp) |
|---|---|---|
| Statico congelato (EOF e SCR 2021 invariati) | 285,44% | +32,18 |
| Semi-statico: solo EOF aggiornato | 288,32% | +35,06 |
| Semi-statico: solo SCR aggiornato | 250,73% | −2,53 |
| Dinamico (EOF e SCR ricalcolati) | 253,26% | 0,00 |

## 2. Bridge EOF 2021→2022 (EUR k)
| Componente | Valore |
|---|---|
| ΔEOF totale | +128.060 |
| Δ Excess of assets over liabilities (S.02.01.02 R1000) | −247.519 |
| Δ Passività subordinate in BOF (AT1 26/7/21 €300 mln + 3/8/22 €500 mln) | +428.240 |
| Δ Reconciliation reserve + altri effetti (residuo) | −52.661 |
Check: −247.519 + 428.240 − 52.661 = +128.060 OK

## 3. Bridge TP 2021→2022 (EUR k, lordo SII pre-TMTP solo-entity: 153.028.806 → 132.733.970)
| Componente | Valore |
|---|---|
| ΔTP lordo SII | −20.294.836 (−13,3%) |
| Effetto azzeramento TMTP (verifica quadriennale) | +1.590.076 |
| Effetto VA 19bps su TP | −565.931 |
| Δ Investimenti | −18.638.984 (−12,4%) |

## 4. Duration implicite [E-derived, shift ~+250bp]
- D_L ≈ 5,30; D_A ≈ 4,94; gap ≈ −0,36
- Previsto ΔExcess ≈ −1,66 mld; effettivo −0,25 mld → contributo dinamico +1,41 mld (VA, DPHB, spread, credit)

## 5. Stress replay "VA azzerato" (LTG-dependency)
| Anno | Ratio base | Ratio senza VA | Delta |
|---|---|---|---|
| 2021 | 285,4% | 279,0% | −6,4 pp |
| 2022 | 253,26% | 239,1% | −14,2 pp |
Dipendenza dal VA più che raddoppiata: 19bps valgono 14pp di ratio nel 2022.

## 6. Assorbimento SCR 2022 (S.25.01.22 lordo)
- BSCR 17.184.931; LAC TP −11.299.794 (65,8% del BSCR) → SCR 5.055.992
- Market risk lordo 7.613.259; life UW lordo 13.469.741: assorbiti via partecipazione agli utili (DPHB)

## 7. Implicazioni per la tesi
1. Il motore statico congelato sbaglia di +32pp: inutilizzabile per monitoring intraday/intra-year.
2. L'errore dominante NON e l'EOF (+128 mln) ma il SCR (+615 mln, quasi tutto life UW): il rischio dinamico chiave e il comportamento riscatti (DPHB).
3. LTG-dependency prociclica: VA vale 6pp nel 2021 e 14pp nel 2022 → il framework dinamico deve prezzarla esplicitamente.
4. TMTP: 1,59 mld nel 2021, azzerato dalla verifica quadriennale nel 2022, proprio quando serviva.
5. Metrica SPS: confrontare bridge EOF effettivi vs previsti per singolo motore, MAE sui ponti EOF/SCR.

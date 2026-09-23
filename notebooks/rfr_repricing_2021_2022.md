# Curve EIOPA RFR EUR — riprezzamento reale del backtest 2021-2022

Sostituisce lo shift [E] +250bp del notebook `backtest_2022_static_vs_dynamic.md` con i movimenti reali
della curva EIOPA EUR (no_VA e with_VA, nodi 1-20). Dati [O] in `data/processed/rfr_curves_eur_2021_2022.csv`
(quality=verified). Derivazioni [E-derived] dichiarate.

## 1. Il VA EIOPA EUR è PIATTO per data (cross-validation)

| Data | VA (bps, nodi 1-20) | Verifica |
|---|---|---|
| 31/12/2021 | 3 (uniforme) | confermato dall'SFCR 2021 (S.22.01.22, impatto TP 217.453) |
| 31/05/2022 | 14 (uniforme) | — |
| 30/09/2022 | 17 (uniforme) | — |
| 31/12/2022 | 19 (uniforme) | ✓ identico al VA dichiarato in SFCR 2022 |

## 2. Shifts reali vs 31/12/2021 (no_VA, bps)

| Nodo | 31/05/2022 | 30/09/2022 | 31/12/2022 |
|---|---|---|---|
| 2 | +138 | +312 | +369 |
| 5 | +151 | +296 | +322 |
| 10 | +157 | +279 | +289 |
| 20 | +141 | +224 | +231 |
| media 1-20 | +150 | +273 | +291 |

Lo shock fu **front-loaded** (breve > lungo) e il picco fu Q3-Q4: lo shift [E] +250bp sottostimava
il rialzo medio reale (+291-307bps) e ne ignorava la forma.

## 3. Riprezzamento con curva reale (sostituzione [E] +250bp)

Metodo [E-derived]: prima approssimazione duration-based uniforme sui nodi 1-20,
D_L = 5,30 e D_A = 4,94 (dal notebook), shift medio with_VA 2021→2022 = +307,5bps.

- ΔBEL solo-tasso = −5,30 × 151.468.375k × 3,075% ≈ **−24,7 mld €**
- ΔBEL osservato [O] = 128.350.704 − 151.468.375 = **−23,1 mld €**
- residuo non-tasso ≈ **+1,6 mld €** (runoff, nuovi affari, aggiustamento DPHB)
- Attivi (inv. 150.845.818k, D_A 4,94): +22,9 mld €
- **Contributo dinamico netto ≈ −1,8 mld €** (con lo shift [E] +250bp era +1,41 mld)

Con la curva REALE il segno del contributo dinamico si inverte: il rialzo effettivo medio (+308bps)
supera la soglia di pareggio duration-gap ([D_L−D_A]×base/shift) implicita nello shift [E] +250bp.
Il motore statico con shift presidiato sottostima quindi l'impatto anche di segno.

## 4. Duration implicita dal VA: la scoperta DPHB [E-derived]

Duration implicita = impatto VA su TP / (TP × VA in decimale):

| Data | TP [O] | VA | Impatto VA→0 su TP [O] | D implicita |
|---|---|---|---|---|
| 31/12/2021 | 151.694.417 | 3 bps | 217.453 | 4,78 |
| 31/12/2022 | 133.029.385 | 19 bps | 565.931 | 2,24 |

La duration effettiva delle passività è quasi ** dimezzata** tra 2021 e 2022. L'ipotesi lineare
(4,78 ≈ D_L=5,30) regge nel 2021 ma NON nel 2022: azzerando il VA la curva sale ma il BEL sale meno
del previsto perché cadono i benefit discrezionali futuri (DPHB). Il cuscinetto DPHB rende la
sensibilità ai tassi **state-dependent** — esattamente ciò che un motore dinamico riprezza e un
motore statico congela. Coerente con il finding principale del backtest (SCR life UW via DPHB).

## 5. Quality flags
- `rfr_curves_eur_2021_2022.csv`: quality=verified, 4 date × 20 nodi × 2 sheet, fonte per riga.
- Questo file sostituisce i nodi sintetici di `macro_series.csv`: migrare i dati verificati e
  marcare `macro_series.csv` come superato o aggiornarne il flag (da fare in locale, il file
  non è leggibile via API in questa sessione).
- Estrazione: userLibrary read + parsing per riga del CSV di conversione xlsx, fogli
  RFR_spot_no_VA / RFR_spot_with_VA, colonna "Euro" (3ª). Notazione scientifica gestita (es. 4e-05).

# Stima empirica del parametro gamma (DPHB lapse) — Poste Vita Group, 2021-2022

**Tag: [E-model] derivato esclusivamente da input [O] tracciati. Nessun numero inventato.**

## 1. Modello

Il DPHB di Poste Vita (descritto in SFCR 2021 §Non-financial assumptions, EN doc b60d9d3a;
RU 2021 IT §e. Dynamic Policy Holder Behaviour, doc a6572589) definisce un fattore moltiplicativo
sulle frequenze di riscatto osservate in funzione di una variabile finanziaria "spread"
(correlazioni non lineari, calibrazione su rendimento retrocesso GS). La forma funzionale interna
non è pubblicata; adottiamo la forma standard esponenziale:

    q(s) = q0 * exp(gamma * (s - s0))

con s = spread BTP-Bund (proxy [E] della variabile "spread" interna, che include il rendimento
retrocesso della Gestione Separata).

## 2. Input [O] (tutti in data/interim/lapse_flows_pvg.csv)

| Dato | 2021 | 2022 | Fonte |
|---|---|---|---|
| Riscatti pagati (€ mln) | 4169.5 [E-derived] | 5.245,2 [O] | SFCR PVG 2022 §5 (+25,8%) |
| Tasso riscatto / riserve iniziali | 3,1% [O] | 3,6% [O] | SFCR PVG 2022 §5 |
| Spread BTP-Bund medio (bps) | 135 [O-text] | 211 [O-text] | macro_vectors_alignment.md |
| Premio riassicurativo mass lapse (€ mln) | n.d. | 21,5 [O] | SFCR PVG 2022 §5 |
| SCR lapse risk (k€) | 1.540.770 [O] | n.d. (OCR) | SFCR PVG 2021, risk profile |

## 3. Stima

- Misura pulita (tasso su riserve, controlla la crescita del portafoglio):
  m = 3,6/3,1 = 1.161; ln(m) = 0.1495;
  Delta-s = 76 bps = 0,0076
  **gamma_low = ln(m)/Delta-s = 19.7** per unità di spread
- Bound superiore (importi lordi, include effetto portafoglio):
  m = 1,258; **gamma_high = 30.2**
- **Stima puntuale: gamma ≈ 19.7 (proxy pulito), banda [19.7, 30.2]**
  equivalenti a **0.197 per 100 bps** di spread.

## 4. implicazioni per lo shock 2022 (+307 bps intraday-shock, +76 bps anno medio)

- Moltiplicatore per +100 bps: x1.22 (ratio) - x1.35 (amount)
- Moltiplicatore per +307 bps: x1.83 - x2.53
- Lapse rate sotto shock completo: 3,1% -> ~5.7% [E-model]

## 5. Caveat accademici

1. La variabile "spread" interna PVG incorpora il rendimento retrocesso della GS, non il solo
   BTP-Bund: la proxy è [E], direzione conservativa (il legame con la GS attenua la sensitività).
2. Due sole osservazioni annue: la stima è una calibrazione puntuale, non una regressione.
   Estendibile con 2019-2020 (SCR lapse 925.628k 2020 già [O]) e 2023 (riscatti in ulteriore
   aumento, Arca 2023 conferma il regime come fenomeno di mercato).
3. La misura "amount-based" (x1,258) sovrastima gamma per effetto crescita premi multiramo;
   la misura "ratio-based" (x1,161) è quella da usare nel motore dinamico.
4. Il premio mass-lapse 2022 (21,5 mln, [O]) è evidenza indiretta che la compagnia stessa
   ha inserito lo shock comportamentale nel pricing del rischio: coerente con gamma > 0.

## 6. Uso nel motore dinamico

Regime LIFE_TRAD (models/lapse_params.md): gamma = 19.7 (central), con stress
triangolare [19.7, 24.9, 30.2] in run di sensitività.
Il motore statico invece congela q = 3,1% (base 2021): sotto lo stesso shock sottostima i
riscatti del 45% [E-model].

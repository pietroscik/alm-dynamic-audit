# Panel inter-compagnia [O] — ALM Dynamic Audit

Campione: 6 compagnie italiane, 3 motori di calcolo diversi, range di taglia 1:400.
Tutti i valori in EUR k (o mln dove indicato), tracciati a (documento, sezione/QRT).
Ratio contrassegnati: O = dichiarato, E = derived EOF/SCR [O].

## Serie solvency ratio

| Anno | PV Group | Arca Vita (MIP) | ISV Group | ISPA Group |
|---|---|---|---|---|
| 2020 | 299,3% | 323,0% [O] | n.d. (SCR 3.957.333) | — |
| 2021 | 285,4% | 291,5% [E] | n.d. (SCR 3.914.538) | — |
| 2022 | 253,3% | **312,0% [E]** | 203,0% [E] | — |
| 2023 | 307,1% | 233,9% [E] | 246,9% [E] | — |
| 2024 | 322,6% | 241,0% [O] | — | 242,7% [E] |
| 2025 | — | 254,0% [O] | — | 259,9% [E] |

## Deduzioni (il cuore dell'analisi campionaria)

### 1. Stesso shock, direzioni OPPOSTE
Nel 2022, con la stessa curva EIOPA (+307bps) e lo stesso VA (19bps):
- PVG: ratio **−32,2pp** (285→253) — SCR life UW esplode via DPHB
- Arca Vita: ratio **+20,5pp** (291→312) — SCR MIP scende (252.912 da 264.833) e EOF sale
Un motore statico congelato al 2021 avrebbe sbagliato **in direzioni opposte** sulle due
compagnie. L'eterogeneita' della risposta NON e' rumor: e' struttura (motore di calcolo,
mix prodotti, DPHB, taglia).

### 2. Il VA e' sistemico, l'impatto no
VA EIOPA dichiarato da Arca: 7 (2020), 3 (2021), 19 (2022), 20 (2023), 23 (2024), 14 (2025) bps.
I valori 2021 (3) e 2022 (19) coincidono ESATTAMENTE con le curve EIOPA estratte
(rfr_curves_eur_2021_2022.csv) [cross-check OK]. Il VA e' un fattore di mercato comune,
ma il suo impatto dipende dal modello: per PVG vale −6,4pp sul ratio nel 2021, per altri
portafogli percentuali diverse. RegTech: il VA va riprezzato, non congelato.

### 3. Tre motori, tre letture dello stesso rischio
- PVG: Standard Formula + DPHB massiccio (ratio guida: tassi)
- Arca Vita: Modello Interno Parziale (MIP) — SCR meno volatile, EOF guida il ratio
- ISV/ISPA: Standard Formula con add-on (30-176 mln) e LAC TP enorme (−5,4 mld nel 2022)
Un audit statico unico presuppone un motore unico: campionando 6 compagnie si vede che
non esiste. Il framework dinamico deve essere model-aware.

### 4. Effetto taglia confermato sul campione allargato
EOF 2024: da 60.172 (Net) a 13.920.129 (PVG) — 1:231. La volatilita' del ratio cresce
al calare della taglia (Net ±6pp/anno su base minuta; PVG ±32pp su base grande ma con
driver di mercato). Stress uniformi proporzionali non sono comparabili.

### 5. Correzioni di rotta 2023-2025
- Arca: SCR +125 mln nel 2023 (+50%) da 378→[driver MIP: rischio di riscatto 2025]
- ISV: SCR −582 mln nel 2023 (4.537→3.955) con EOF +552: ratio +44pp
- ISPA: EOF +1.525 mln nel 2025 (emissioni subordinate)
Dinamiche di imprese diverse per natura: l'audit statico le appiattisce.

## Open item
- ISV 2020/2021: celle ratio OCR-corrotte (R0690 "22.4%", "2095"); EOF non ricostruibile
  con certezza -> n.d. (da QRT S.23.01.22 originale)
- ISPA perimetro: il dato 2023 (9.373,7 vs "diminuzione di 388 da 9.762") e' ambiguo nel
  testo; 2024/2025 solidi
- ISPA 2025 LAC TP R0140 = +5.734.690: segno sospetto (atteso negativo) — da verificare

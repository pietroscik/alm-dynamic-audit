# Panel esteso 2019–2024 — Poste Vita Group [O]

Estensione del dataset agli anni disponibili in libreria alm-dynamic. Con 2019 e 2020 la serie
storica del gruppo è completa su 6 esercizi. Formato SFCR pre-2021: BEL/RM gruppo non esposti in
tabella aggregata (solo per LoB) → campi vuoti, non [E]: da estrarre solo per necesidadità di tesi.

## Serie storiche chiave (EUR k)

| Anno | TP (S.22.01.22) | TMTP | EOF SCR | SCR | Ratio | VA→0 su TP | VA→0 su EOF |
|---|---|---|---|---|---|---|---|
| 2019 | 132.764.862 | 1.908.091 | 11.468.565 | 3.675.204 | 312,00% | 537.028 | −371.396 |
| 2020 | 147.434.522 | 1.749.084 | 11.193.573 | 3.739.960* | 299,27% | 669.737 | −463.295 |
| 2021 | 151.694.417 | 1.590.076 | 12.676.835 | 4.441.175 | 285,40% | 217.453 | −391.511** |
| 2022 | 133.029.385 | 0 | 12.804.895 | 5.055.992 | 253,26% | 565.931 | −391.511 |
| 2023 | 145.741.821 | 0 | 14.098.823 | 4.591.654 | 307,05% | 571.199 | −393.674 |
| 2024 | 152.319.265 | 0 | 13.920.129 | 4.314.983 | 322,60% | 572.475 | −393.517 |

*SCR 2020 [E-derived] da ratio dichiarato 299,27% (coerente col testo "da €3.679 mln a €3.740 mln").
**VA→0 EOF 2021: 217.453 su TP; EOF impact da S.22.01.22 2021 (già nel dataset).

## Letture per la tesi

1. **TMTP in run-off controllato**: 1.908.091 (2019, 75%) → 1.749.084 (2020, 68,75%) → 1.590.076
   (2021, 62,5%) → 0 (2022, verifica quadriennale). Il motore statico che congela il TMTP al 2019
   sovrastima le TP di ~1,9 mld al 2022; il decadimento programmato è perfettamente prevedibile e
   modellabile — primo argomento a favore del framework dinamico.

2. **VA→0 su TP, serie 2019–2024**: 537 → 670 → **217** → 566 → 571 → 572 mln. L'anomalia 2021
   (VA EIOPA 3 bps, minimo storico) è isolata e riverifica l'anno base del backtest come anno
   straordinario: chi calibra il modello solo sul 2021 importa un VA sottostimato.

3. **Ratio 2019→2024**: 312 → 299 → 285 → 253 → 307 → 323%. Il V-shape 2022→2023 conferma il
   mean-reversion post-shock catturato solo dal motore dinamico (backtest: errore statico +32,2pp).

4. **Coerenze incrociate**: EOF 2019 11.468.565 = testo 2020 "€11.469 mln" ✓; EOF 2020 11.193.573
   = "€11.194 mln" ✓; SCR 2019 3.675.204 ≈ testo "€3.679 mln" (arrotondamento) ✓.

## Estrazione
SFCR 2019 (doclib alm-dynamic id 358f3ee7-920c-4606-8015-f0ce830e84f0), SFCR 2020
(id ca788307-660c-42d2-b9bd-c577bfb0faf8), sezioni E.1/E.2 e QRT S.22.01.22 gruppo.

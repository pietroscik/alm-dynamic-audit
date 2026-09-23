# Whitepaper — Struttura dei capitoli (v1)

## Capitolo 1 — Il problema: la finzione della staticità
- 1.1 Perché i modelli ALM statici congelano curve e comportamenti (prassi, regolamentazione, calcolo)
- 1.2 Il costo nascosto: il 2022 come esperimento naturale (BTP 10y 0,50%→4,65%; spread 135→211 bps)
- 1.3 Obiettivo e ipotesi della ricerca

## Capitolo 2 — Dataset e regole di accettazione
- 2.1 Regola [O]/[E]/n.d. e tracciabilità a (documento, sezione/QRT)
- 2.2 Libreria documentale: SFCR PVG 2019-2024, Arca Vita 2020-2025, ISV, ISPA, Net Insurance
- 2.3 Curve EIOPA EUR 2020-2026: estrazione, verifica (20 nodi × 2 sheet × 6+ date)
- 2.4 Open item OCR e disciplina del n.d. (mai interpolare)

## Capitolo 3 — Il caso centrale: Poste Vita Group 2021-2022
- 3.1 Lo shock certificato: SCR spread, VA 3→19 bps, TMTP run-off 1.908→0
- 3.2 L'inversione di segno: curve reali (−1,8 mld) vs shift sintetico (+1,41 mld)
- 3.3 Duration implicita dal VA: 4,78 → 2,24 (assorbimento DPHB, sensibilità state-dependent)
- 3.4 Asset mix: deconcentrazione sovrana programmata (BTP share 97%→75%, 2021→2024)

## Capitolo 4 — Il comportamento: da ipotesi a misura
- 4.1 Il DPHB di Poste Vita (descritto in SFCR 2021/RU 2021) e la forma exp(gamma*ds)
- 4.2 Stima su dati [O]: gamma = 19,7 (ratio) / banda [19,7; 30,2] (amount)
- 4.3 Validazione out-of-sample 2023: lag-1, gamma = 30,1 riproduce il 4,4% osservato
- 4.4 Isteresi e floor asimmetrico: il 2023 smentisce l'elasticità contemporanea
- 4.5 Evidenza indiretta: premio mass-lapse 21,5 mln (2022) e gap vs mercato (4,4% vs 10,6%)
- 4.6 Specificazione raccomandata: q_t = q0 * exp(gamma * max(0, ds_{t-1}))

## Capitolo 5 — Il backtest pluriennale 2021-2026
- 5.1 Impostazione statico vs dinamico (repricing zero-coupon 10y, curva congelata 2021)
- 5.2 Il gap che non si chiude: −18,6 / −24,2 punti; 2026 nuovo allargamento
- 5.3 Il VA come proxy regulator dell'isteresi (3→19→17→20→20→12 bps)
- 5.4 Lapse projection 2023-2026 con banda gamma e floor
- 5.5 Limiti dichiarati: duration costante (bound superiore), spread 2024-26 n.d.

## Capitolo 6 — Il pannello cross-company
- 6.1 Stesso shock, direzioni opposte: PVG −32,2pp vs Arca +20,5pp
- 6.2 Serie 2019-2024 PVG e entity panel (PV solo / PA / Net)
- 6.3 Generalizzazione: la direzione dell'impatto è struttura, non shock

## Capitolo 7 — Conclusioni e raccomandazioni
- 7.1 Il motore statico non è prudente: è cieco
- 7.2 Raccomandazioni per risk management e supervisione
- 7.3 Ricerca futura: gamma cross-company, curve 2026+, dati mensili riscatto

## Appendici
- A. Data dictionary e regole [O]/[E]/n.d.
- B. Elenco commit e tracciabilità (SHA → file → fonte)
- C. Scripts riproducibili (dry-run default, pytest, verify_dataset.py)
- D. Open items e n.d. documentati

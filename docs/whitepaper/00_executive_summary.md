# ALM Dynamic Audit — Executive Summary

**Poste Vita Group 2021-2026: perché un motore ALM dinamico batte un motore statico.**
Dataset: pietroscik/alm-dynamic-audit (main). Regola di accettazione: nessun numero [O] (osservato)
se non tracciato a (documento, sezione/QRT); tutto il resto è [E]/[E-model] o n.d. Mai interpolato.

## Tesi in una frase

Il rialzo dei tassi 2022 non è stato un episodio transitorio ma un cambio di regime permanente:
un motore statico che congela curve e comportamenti al 31.12.2021 ha vissuto il quinquennio
successivo in una realtà parallela, con errori di repricing sistematici (−18,6 / −24,2 punti su
portafoglio 10y) e una sottostima strutturale dei riscatti (~26-32% [E-model]).

## I quattro pilastri empirici

1. **Inversione di segno del contributo dinamico.** Con le curve reali EIOPA il contributo di
   riprezzamento 2022 è −1,8 mld € (duration implicita 4,78 → 2,24, assorbimento DPHB); con lo
   shift sintetico [E] +250bp sarebbe +1,41 mld. Le curve reali invertono il segno della
   conclusione analitica: le approssimazioni lineari non sono conservative, sono sbagliate.
2. **Stesso shock, direzioni opposte.** +307bps (2022, VA 19bps): PVG ratio −32,2pp, Arca Vita
   +20,5pp. Il driver è la struttura attivi/passivi e il comportamento, non lo shock in sé —
   ciò che un motore statico congela e uno dinamico aggiorna.
3. **Comportamento calibrato, non ipotizzato.** gamma (DPHB lapse) stimato su dati [O]
   SFCR: 19,7 (misura pulita su ratio) con banda [19,7; 30,2]; validato out-of-sample nel 2023
   (gamma_lag = 30,1 riproduce esattamente il 4,4% osservato su riserve medie). Evidenza
   indiretta: premio riassicurativo mass-lapse 21,5 mln € pagato proprio nel 2022 [O].
4. **Isteresi comportamentale e di mercato.** Nel 2023 lo spread si restringe (214→166 bps)
   ma i riscatti salgono (3,5%→4,4%): la specificazione contemporanea è rigettata, quella
   lag-1 con floor asimmetrico è validata. Il VA EIOPA segue la stessa isteresi
   (3→19→17→20→20→12 bps, 2021-2026): due serie indipendenti, una sola dinamica.

## Il verdetto del quinquennio (backtest 2021-2026)

| Data | r10 no-VA | VA | P dinamico | P statico | Gap |
|---|---|---|---|---|---|
| 12/2021 | 0,205% | 3 bps | 97,97 | 97,97 | 0,00 |
| 12/2022 | 3,092% | 19 bps | 73,75 | 97,97 | −24,22 |
| 01/2023 | 2,764% | 17 bps | 76,14 | 97,97 | −21,84 |
| 01/2024 | 2,472% | 20 bps | 78,33 | 97,97 | −19,64 |
| 01/2025 | 2,333% | 20 bps | 79,40 | 97,97 | −18,57 |
| 01/2026 | 2,798% | 12 bps | 75,88 | 97,97 | −22,09 |

Il gap non si chiude mai; nel 2026, col lungo di nuovo a 2,80%, si allarga di nuovo. Nessuna
"transitorietà": cambio di regime. (Curve EIOPA EUR [O, verified], 6 date × 20 nodi × 2 sheet.)

## Perché è inattaccabile

- Ogni numero è tracciato a (documento, sezione): SFCR PVG 2019-2024, Arca Vita 2020-2025,
  ISV, ISPA, Net Insurance; curve EIOPA 2020-2026.
- Le celle OCR corrotte restano n.d. definitivo, documentate (OPEN_ITEMS_CLOSURE.md).
- Il parametro comportamentale non è arbitrario: è stimato su dati ufficiali e validato
  out-of-sample; la banda [19,7; 30,1] è usata come stress triangolare, non come punto.
- PVG è il caso conservativo: 4,4% di frequenza riscatto 2023 vs media mercato 10,6% [O-text,
  Ania Trends 2023]. Il modello non sovrastima: sottostima meno dello statico.
- Riproducibilità: notebooks 01-09, scripts (dry-run di default), QA invarianti con exit≠0
  (verify_dataset.py), pytest.

## Decontestualizzazione del rischio per l'industry

La stessa struttura vale per qualsiasi compagnia con passività vita tradizionali duration-negative
e portafoglio sovrano concentrato: il pannello cross-company (6 compagnie × motori) mostra come
la direzione dell'impatto dipenda dalla struttura, non dallo shock. Il motore statico non è
"prudente": è cieco alla state-dependence.

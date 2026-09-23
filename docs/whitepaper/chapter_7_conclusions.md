# Capitolo 7 — Conclusioni e raccomandazioni

## 7.1 Sintesi delle evidenze

1. **Errore di direzione, non di misura.** Curve reali vs shift sintetico: contributo
   −1,8 mld € contro +1,41 mld € (segno invertito) sul 2022 PVG [E-model su input [O]].
2. **Errore sistematico, non episodico.** Gap statico-dinamico −18,6 / −24,2 punti su
   portafoglio 10y, per 5 rilevazioni consecutive 2022-2026, mai nullo [O-curve].
3. **Comportamento misurato, non ipotizzato.** γ = 19,7-30,1 [E-model], validato
   out-of-sample sul 2023 (4,06-4,40% proiettato, 4,4% osservato [O]), con evidenza
   indiretta convergente (premio mass-lapse 21,5 mln € nel 2022 [O]).
4. **Isteresi duale.** VA EIOPA e riscatti seguono la stessa asimmetria: il narrowing non
   riporta né il VA né i riscatti alla base (2023: spread −48bps, riscatti 3,5%→4,4% [O]).
5. **Cambio di regime.** Nessuna normalizzazione del r10 al livello pre-shock entro il
   2026 (2,80% a gennaio 2026 vs 0,205% congelato): la "transitorietà" è confutata.

## 7.2 Raccomandazioni

**Per il risk management.** (i) Sostituire gli shift costanti con repricing su curve
storiche/ufficiali complete; (ii) calibrare il comportamento su dati interni con lag e
asimmetria dichiarati (la specificazione q_t = q0·exp(γ·max(0, Δs_{t-1})) è un punto di
partenza, non un dogma); (iii) monitorare la duration implicita come indicatore di
state-dependence (misurabile da soli documenti pubblici).

**Per la supervisione e la ricerca.** (i) Richiedere disclosure della specificazione
comportamentale (lag, simmetria) accanto alle frequenze osservate; (ii) trattare il VA
come ciò che è empiricamente: un indicatore con isteresi, informativo sul regime e non
solo sul livello; (iii) estendere il test di stabilità γ a pannelli più ampi.

## 7.3 Limiti

Dichiarati in BACKTEST_2021_2026.md e nei modelli: portafoglio teorico 10y (bound
superiore a duration costante; la duration implicita PVG 4,78→2,24 è essa stessa
endogena); due-tre osservazioni annue per parametro (calibrazione puntuale, non
regressione); spread 2024-2026 n.d. (proiezione a floor, dichiarata); proxy BTP-Bund per
la variabile interna "spread + rendimento retrocesso GS" (conservativa in direzione).

## 7.4 Ricerca futura

(i) γ cross-company su pannello con dati mensili di riscatto; (ii) deconvoluzione della
variabile interna PVG (spread vs rendimento GS); (iii) backtest a duration dinamica con
riequilibrio del portafoglio; (iv) estensione oltre il 2026 con curve EIOPA trimestrali
già nel corpus.

## Chiusura

La staticità non è prudenza: è cecità selettiva. Il quinquennio 2021-2026 ha mostrato che
il mercato cambia regime, che i policyholder rispondono con un anno di ritardo e senza
simmetria, e che tutto questo è misurabile da documenti pubblici. Un motore ALM che non
lo incorpora non è "un'approssimazione accettabile del mondo reale": è una descrizione
di un mondo che non esiste più dal 2022.

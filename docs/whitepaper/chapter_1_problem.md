# Capitolo 1 — Il problema: la finzione della staticità

## 1.1 Perché i modelli ALM statici congelano curve e comportamenti

Un motore ALM statico è una scelta metodologica prima che computazionale. Congelare la curva
dei tassi, le frequenze di riscatto e la struttura del portafoglio alla data di valutazione
significa affermare che il sistema assicurativo sia approssimabilmente *time-invariant* su
un orizzonte rilevante: che le passività di domani si comportino come quelle di oggi,
qualunque cosa faccia il mercato. L'ipotesi ha basi operative legittime (trasparenza di
calcolo, confrontabilità, prudenza apparente), ma è confutabile nei dati — ed è esattamente
ciò che questo lavoro fa.

Le tre fonti della staticità, in ordine di gravità:

1. **Staticità della curva.** Lo shift costante (es. +250bp [E]) sostituisce la dinamica
   reale della struttura per scadenza con una traslazione rigida: perde la forma, la
   convergenza verso l'UFR e la ricorsione dei dati di mercato.
2. **Staticità del comportamento.** Le frequenze di riscatto osservate al tempo t vengono
   proiettate invariate: il policyholder behavior non risponde né ai tassi né alla
   competitività del prodotto.
3. **Staticità della struttura.** Asset mix e duration sono trattati come costanti anche
   quando la compagnia comunica strategie di riallocazione pluriennali (il caso PVG:
   deconcentrazione sovrana programmata, BTP share 97%→75% tra 2021 e 2024 [O SFCR]).

## 1.2 Il 2022 come esperimento naturale

Il biennio 2021-2022 offre condizioni quasi sperimentali per testare queste ipotesi:
una variazione del tasso governativo italiano a 10 anni dallo 0,50% al 4,65% (+346bps)
contro un Bund a 2,54% (+270bps) [O-text, Arca Vita SFCR 2022 §A.3], con uno spread
BTP-Bund che passa da ~135 a 211-214 bps. Un solo esperimento, tre variabili osservabili
in modo indipendente: curva EIOPA (ufficiale, quotidiana), comportamento dei riscatti
(SFCR, annuale) e percezione del rischio della compagnia (premi riassicurativi, SCR).

L'ampiezza e la velocità dello shock — e il fatto che non si sia *inverted*, come il
backtest 2021-2026 dimostra (r10 = 2,80% a gennaio 2026, gap statico di nuovo a −22,1
punti) — rendono il quinquennio 2021-2026 il banco di prova definitivo della staticità.

## 1.3 Obiettivo, ipotesi e criterio di confutazione

**Obiettivo.** Quantificare l'errore sistematico di un motore ALM statico rispetto a uno
dinamico, su dati interamente pubblici e tracciati, nel caso Poste Vita Group, e verificare
se l'errore sia di misura o di direzione.

**Ipotesi H1.** L'approssimazione statica produce errori di repricing sistematici e di
segno costante (non rumore).

**Ipotesi H2.** Il comportamento di riscatto è endogeno al contesto di mercato, con
elasticità misurabile e asimmetrica.

**Criterio di confutazione.** H1 è confutata se il gap statico-dinamico è nullo o di segno
alternante senza struttura; H2 è confutata se il parametro comportamentale stimato su un
periodo non predice out-of-sample. Su entrambe, i dati confermano le ipotesi: il gap è
sistematico (−18,6 / −24,2 punti su portafoglio 10y, mai nullo dopo lo shock) e la stima
γ = 19,7-30,1 [E-model] riproduce il 4,4% osservato nel 2023 [O SFCR PVG 2023].

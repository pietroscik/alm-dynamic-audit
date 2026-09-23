# Capitoli 3-4 — Sezioni chiave (bozza v1)

## 3.2 L'inversione di segno (testo principale)

Il confronto più severo per le approssimazioni statiche non è di grandezza ma di segno.
Valutando il riprezzamento delle passività con le curve EIOPA effettive del 2022 il contributo
dinamico è di −1,8 mld €: la duration implicita delle passività scende da 4,78 a 2,24 e il
DPHB assorbe parte dello shock. Applicando invece lo shift sintetico [E] +250bp su curva 2021
il contributo sarebbe +1,41 mld, segno opposto. La conclusione analitica si inverte al cambio
del metodo di riprezzamento: chi usa lo shift sintetico non commette un errore di misura,
commette un errore di direzione.

## 3.3 Duration implicita e assorbimento DPHB

Il rapporto VA/TP pubblicato nei SFCR consente di ricavare la duration implicita delle
passività a ogni data: 4,78 (2021) → 2,24 (2022). La contrazione non è un effetto di portafoglio
ma di comportamento: il DPHB rende la stessa passività meno duration-sensitive quando lo shock
si materializza. È la definizione operativa di state-dependence, misurabile dai documenti
pubblici senza alcun modello proprietario.

## 4.2-4.4 Dalla stima alla validazione

Stimato gamma sul solo biennio di shock [O] (riscatti 3,1%→3,6% su riserve aperture; spread
BTP-Bund 135→211 bps), il test out-of-sample 2023 è impietoso con la specificazione
contemporanea: lo spread scende ma i riscatti salgono (3,5%→4,4% su riserve medie). La
specificazione lag-1 con floor asimmetrico invece riproduce l'osservazione con gamma = 30,1,
dentro la banda stimata [19,7; 30,2] al suo upper bound. Tre implicazioni:

1. il comportamento non è istantaneo: l'inerzia contrattuale e distributiva del canale postale
   introduce un ritardo di circa un anno;
2. la risposta è asimmetrica: il narrowing non riporta i riscatti alla base (isteresi);
3. il parametro è una misura, non un'ipotesi: chi lo contesta deve spiegare perché due
   specificazioni indipendenti (SFCR riscatti e VA EIOPA) mostrano la stessa isteresi.

Il punto difensivo decisivo: PVG riscatta a 4,4% contro una media di mercato del 10,6%
[O-text, Ania 2023]. Il motore dinamico con gamma>0 resta sotto la metà del mercato: non
c'è sovrastima artificiale del rischio comportamentale.

## 5.2 Il gap che non si chiude (anteprima testo)

Nel quinquennio 2021-2026 il motore statico registra gap zero in ogni data; il motore
dinamico registra −18,6 / −24,2 punti su portafoglio 10y. L'argomento della "transitorietà"
è confutato dai dati: a gennaio 2025 (r10 2,33%) il gap è ancora −18,6 punti e a gennaio 2026
(r10 di nuovo a 2,80%) si allarga a −22,1. La normalizzazione attesa non è arrivata perché lo
shock non era un livello: era un regime.

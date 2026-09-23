# KNOWN_GAPS — Punti ciechi aperti (audit 2026-09-23, post-9d66128)

Audit di forma e sostanza. Punti aperti, in ordine di priorità per la diffusione.

## A. Strutturali (richiedono lavoro locale o decisione)

1. **Duplicazione del motore**: scripts/dynamic_engine.py (γ band [19.7, 30.1], lag-1, floor)
   vs src/dynamic_engine.py (engine preesistente). Rischio divergenza: due implementazioni
   dello stesso modello. Azione: verificare localmente quale è la fonte di verità; se src/
   è usato da app/app.py, portarvi la specificazione lag-1 con floor oppure deprecare
   scripts/ a favore di src/ con i parametri nuovi. NON sovrascritto da remoto (contenuto
   src/ non leggibile via API: solo SHA).
2. **data_dictionary.csv (radice)**: non aggiornato con le metriche lapse/backtest; esiste
   solo l'addendum. Azione: merge locale (cat addendum >> data_dictionary.csv, o merge tool).
3. **Nessuna CI** (.github assente): verify_dataset.py e pytest non sono gate automatici.
   Azione: GitHub Actions con python scripts/verify_dataset.py && pytest (exit≠0 già previsto).
4. **Nessun LICENSE e nessun tag/release**: bloccanti per diffusione accademica/pubblica.
5. **README.md**: verificare che rifletta la struttura attuale (whitepaper, 3 script,
   9 notebook, pannelli) — non modificato da remoto per non sovrascrivere.

## B. Metodologici (dichiarati ma da sorvegliare in diffusione)

6. **Misure lapse non omogenee**: 2021-22 su riserve aperture (3,1/3,6), 2022-23 su riserve
   medie (3,5/4,4). La stima γ lag-1 usa la serie media-riserve; il confronto con la banda
   [19,7-30,2] (stimata su aperture) è indicativo, non identico per costruzione. Già
   dichiarato nei models/, va ribadito a voce se contestato.
7. **Definizione "lapses" SFCR 2023**: il +1,7 mld è voce IFRS17/lapse che può includere
   riscatti parziali e riduzioni; il 2022 "surrenders" (5.245,2) è voce settlement. Il
   dato 2023 (6.945 [E-derived]) è quindi un upper bound di confronto approssimato.
8. **Curve gennaio vs dicembre**: il backtest mescola rilevazioni 31.12 (2021, 2022) e
   31.01 (2023-2026). Distanza di un mese: non influenza la direzione, ma dichiararlo.
9. **Repricing no-VA**: il confronto statico/dinamico usa curve no-VA; i SFCR valutano TP
   con VA. Coerente internamente (stessa base), ma il gap −18,6/−24,2 è in termini no-VA.
10. **Spread 2024-2026 n.d.**: proiezione lapse a floor dichiarata [E-model], mai interpolata.
11. **γ su 2-3 osservazioni annue**: calibrazione puntuale; la banda è stress triangolare,
    non intervallo di confidenza statistico.
12. **Portafoglio teorico 10y**: bound superiore a duration costante; la duration implicita
    PVG (4,78→2,24) è essa stessa endogena. Già in BACKTEST_2021_2026.md §5.

## C. Documentali

13. INTEGRITY_REPORT.md fermo a 02edd20: aggiornare dopo il merge locale finale (o
    rigenerare pre-release come snapshot finale).
14. I commit pre-616c60f (infrastrutturali: 2ac1de0…7aec972) non hanno riga in Appendice B:
    accettabile (nessun dato), ma una nota "infrastruttura, nessun contenuto dati" evita
    l'osservazione "perché questi SHA non sono tracciati?".

Regola: questo file si chiude solo quando ogni punto ha risoluzione o è promosso a
limitazione dichiarata permanente (Appendice D).

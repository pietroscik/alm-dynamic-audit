# KNOWN_GAPS — Punti ciechi (audit 2026-09-23; aggiornato dopo commit di consolidamento)

## A. Strutturali

1. ~~Duplicazione del motore~~ → **APERTO (richiede locale)**: scripts/dynamic_engine.py
   (γ band, lag-1, floor) vs src/dynamic_engine.py (engine dell'app). Contenuto src/ non
   leggibile via API: decisione locale — portare la specificazione lag-1+floor in src/
   oppure dichiarare scripts/ riferimento metodologico e src/ runtime. Verificare che
   app/app.py usi la specificazione validata.
2. ~~data_dictionary.csv non aggiornato~~ → **APERTO (merge locale)**:
   cat data_dictionary_addendum_lapse_backtest.csv >> data_dictionary.csv
   (oppure merge con controllo colonne).
3. ~~Nessuna CI~~ → **CHIUSO**: .github/workflows/ci.yml (verify_dataset +
   verify_new_datasets + pytest su push/PR).
4. ~~Nessun LICENSE/release~~ → **CHIUSO (LICENSE MIT)**; manca il tag v1.0: da creare
   dopo il sync locale e CI verde.
5. ~~README non allineato~~ → **CHIUSO**: riscrittura completa (nota: sovrascrive la
   versione precedente non leggibile via API; eventuale contenuto perso recuperabile da
   git history).
6. ~~verify_dataset non copre i CSV nuovi~~ → **CHIUSO**: scripts/verify_new_datasets.py
   (invarianti curve 2023-26, backtest, tracciabilità lapse), eseguito in CI.

## B. Metodologici → **CHIUSI come perimetro dichiarato**

7. MET-1..MET-7 promossi in Appendice D §D.2 (limitazioni dichiarate con effetto
   direzionale): misure lapse non omogenee, lapses-vs-surrenders, rilevazioni 31.12/31.01,
   repricing no-VA, portafoglio teorico 10y, γ su 2-3 osservazioni, proxy BTP-Bund.

## C. Documentali

8. ~~Appendice B senza nota sui commit infrastrutturali~~ → **CHIUSO**: nota aggiunta.
9. INTEGRITY_REPORT.md → snapshot aggiornato con questo commit; rigenerare solo dopo il
   merge locale finale (ultima azione pre-tag v1.0).

## Riepilogo stato

CHIUSO da remoto: 3, 4 (LICENSE), 5, 6, 7, 8. APERTO in locale: 1 (dual-engine), 2
(merge dictionary), tag v1.0 dopo CI verde. Nessun altro punto ciechio noto.

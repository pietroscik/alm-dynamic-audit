# ALM Dynamic Audit

Backtest statico vs dinamico su dati interamente pubblici e tracciati.
Caso centrale: **Poste Vita Group 2021-2026**; pannello: Arca Vita, ISV, ISPA, Net Insurance.

## Tesi

Il rialzo dei tassi 2022 e' un cambio di regime permanente, non un episodio transitorio.
Un motore ALM statico (curva e comportamenti congelati al 31.12.2021) produce errori di
repricing sistematici (-18,6 / -24,2 punti su portafoglio 10y, 2022-2026) e una sottostima
strutturale dei riscatti. Le curve reali EIOPA invertono il segno del contributo dinamico
rispetto a uno shift sintetico (+250bp): -1,8 mld € contro +1,41 mld €.

## Risultati chiave

- **gamma (DPHB lapse) stimato su dati [O]**: 19,7 centrale, banda [19,7; 30,1]; lag-1 con
  floor asimmetrico, validato out-of-sample sul 2023 (proiettato 4,06-4,40%, osservato 4,4%).
- **Backtest 2021-2026**: gap statico-dinamico mai nullo dopo lo shock; nuovo allargamento
  a gennaio 2026 (r10 = 2,80%).
- **Isteresi duale**: VA EIOPA (3→19→17→20→20→12 bps) e riscatti seguono la stessa asimmetria.
- **Pannello**: stesso shock (+307bps), direzioni opposte (PVG -32,2pp vs Arca +20,5pp):
  l'impatto e' funzione della struttura, non dello shock.

## Regola di accettazione dei dati

Nessun numero entra come [O] (osservato) se non tracciato a (documento, sezione/QRT).
Il resto e' [E]/[E-model] con formula dichiarata, oppure n.d. — mai interpolato.
Dettagli: docs/whitepaper/appendix_a_data_dictionary.md, appendix_d_open_items.md.

## Struttura

- `data/interim`, `data/processed` — CSV tracciati + SOURCES (7 addendum)
- `models/` — lapse params, stima gamma, test di stabilita' [E-model]
- `scripts/` — integrate_rfr_macro (dry-run default), verify_dataset, verify_new_datasets,
  dynamic_engine (gamma band, lag-1, floor)
- `src/` — moduli engine dell'app (dynamic_engine, static_engine, liquidity, sps...)
- `app/app.py` — dashboard Streamlit
- `notebooks/01-09` — analisi riproducibili
- `docs/whitepaper/` — executive summary, capitoli 1-7, appendici A-D,
  INTEGRITY_REPORT, matrice di tracciabilita' (Appendice B)
- `KNOWN_GAPS.md` — punti ciechi aperti e loro stato

## Quickstart

```bash
pip install -r requirements.txt
python scripts/verify_dataset.py          # invarianti core
python scripts/verify_new_datasets.py     # invarianti curve 2023-26 + backtest + lapse
pytest tests/ -q
python scripts/dynamic_engine.py --q0 3.5 --dspread-bps 76
streamlit run app/app.py
```

## Attribuzione

Poste Vita funge da benchmark di stress-test, non da unicum: l'architettura e' replicabile
su qualsiasi portafoglio con SFCR pubblici; i parametri (gamma) vanno ri-stimati per
portafoglio. Vedere docs/whitepaper/chapter_6_panel.md §6.4 e 00_executive_summary.md
("Ambito di generalizzazione").

## Licenza

MIT — vedere LICENSE. I documenti sorgente (SFCR, curve EIOPA) NON sono ridistribuibili
con il repo: la tracciabilita' resta nei file SOURCES con doc-ID (data/raw resta vuoto).

## Citazione

Maietta, P. (2026). *ALM Dynamic Audit: un motore dinamico contro la finzione della
staticita'. Backtest 2021-2026 su dati pubblici tracciati.* Repository + whitepaper.

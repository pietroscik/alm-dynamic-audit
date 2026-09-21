# ALM Dynamic Audit

## Obiettivo
Misurare empiricamente in che misura un framework ALM statico — basato su
ipotesi lineari e lapse rate costanti — sottostimi la vulnerabilita'
economica e di liquidita' delle compagnie vita italiane rispetto a un
motore dinamico mark-to-market con comportamento endogeno.

## Domanda di ricerca
L'utilizzo di modelli semplificati e statici nell'assicurazione vita
nasconde rischi sistemici (blind spots) in scenari di shock combinato
(tassi al rialzo, allargamento dello spread, aumento dei riscatti)?
Se si, di che entita' economica parliamo?

NOTA METODOLOGICA: il motore dinamico e' costruito per VERIFICARE se e in
che misura le non linearita' producano vulnerabilita' aggiuntiva rispetto
al benchmark statico. Il segno del delta e' un OUTPUT, non un presupposto.

## Architettura (layered design)
1. Dati e ingestion (data/, src/data_loader.py, src/eiopa_loader.py,
   src/data_quality.py): dati osservati 2021-2022 da SFCR Solvency II e
   curve macro EIOPA. Pipeline raw -> interim -> processed.
2. Core motori (src/):
   - cashflow_builder.py: flussi sintetici coerenti con duration osservate
   - static_engine.py: immunizzazione lineare ortodossa (benchmark)
   - dynamic_engine.py: M2M nodo per nodo con lapse endogeno
   - liquidity_engine.py: costi di liquidazione (fire sales)
   - sps_calculator.py: punteggio composito esplorativo
3. Frontend e audit (app/app.py): dashboard Streamlit.

## Tracciabilita' dei dati (framework O/D/E)
Ogni variabile e' classificata come:
- O - Observed: dati di mercato o bilancio, con fonte (file, pagina, riga)
- E - Estimated/Proxy: parametri ricostruiti con metodo dichiarato
- D - Derived: output calcolato dai motori
Il tracciato completo e' in data_dictionary.csv.
REGOLA DI ACCETTAZIONE: un numero entra come [O] solo se e' tracciabile a
(file, sezione/pagina, riga, colonna). Altrimenti e' [E] con metodo, o non entra.

## Criterio di selezione del campione (dichiarato ex ante)
- Compagnia 1: Poste Vita S.p.A. (Single SFCR, perimetro vita, standard
  formula, distribuzione bancopostale, prevalenza Ramo I/III).
- Compagnia 2: da registrare qui PRIMA dell'apertura dei PDF. Candidati:
  Arca Vita (mid-cap bancassicurativo, profilo passivita' analogo) oppure
  Intesa Sanpaolo Vita (large cap, disclosure di qualita').
- Finestra: 2021-2022, frequenza annuale, scenario centrale: stress 2022.

## Stato dei dati
ATTENZIONE: i CSV in data/processed/ sono un PILOTA SINTETICO per il
dry-run della pipeline (flag quality_note = synthetic / approx).
NON sono dati osservati. Prima del backtest definitivo vanno sostituiti
con: (1) curve EIOPA dai file Excel ufficiali (eiopa_loader.py),
(2) estrazione SFCR compilando data/interim/company_sfcr_interim.csv.

## Limitazioni dichiarate
- I flussi di cassa contrattuali granulari non sono pubblici: vengono
  approssimati con flussi sintetici coerenti con duration e aggregati
  osservabili.
- Curva a 10 nodi annui (MVP); finestra di liquidita' annua.
- Lapse a un fattore; parametri gamma/haircut non calibrati (sensitivity
  analysis richiesta).
- La copertura riassicurativa del mass lapse (dichiarata da Poste Vita)
  mitiga parte del blind spot stimato: il risultato e' un upper bound.
- Il framework quantifica l'ordine di grandezza del blind spot sotto
  assunzioni dichiarate; non misura una compagnia specifica.

## Esecuzione
pip install -r requirements.txt
pytest tests/
streamlit run app/app.py

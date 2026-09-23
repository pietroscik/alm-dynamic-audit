# Capitolo 2 — Dataset e regole di accettazione

## 2.1 La regola [O]/[E]/n.d.

Il vincolo epistemico del lavoro: nessun numero entra nel dataset come osservato [O] se non
è tracciato a una coppia (documento, sezione/QRT) univocamente reperibile. Tutto ciò che è
derivato è [E] o [E-model] con formula dichiarata; ciò che non è verificabile è n.d.
definitivo, mai interpolato. La regola è applicata in direzione *sfavorevole* alla tesi:
dove l'OCR corrompe un dato (ratio ISV 2020-21), il dato resta n.d. anche se un'inferzione
sarestica sarebbe stata possibile e conveniente (OPEN_ITEMS_CLOSURE.md).

Gerarchia di qualità: [O] numerico (tabella/QRT) > [O-text] numerico nel corpo testo >
[E-derived] inverso aritmetico di un [O] (formula nel campo source_section) > [E-model]
parametro derivato. Ogni CSV del repo espone la colonna *tag* e la coppia *source_doc /
source_section*.

## 2.2 Libreria documentale

Corpus: 29 documenti — SFCR/Relazione Unica Poste Vita Group 2019-2024 (IT/EN), SFCR Arca
Vita 2020-2025, ISV 2020-2023, ISPA 2024-2025, Net Insurance 2022, bilanci affiancati.
Ogni documento è identificato da doc-ID stabile (es. SFCR PVG 2021 EN = b60d9d3a; 2022
EN = 54ddfa37; 2023 EN = 82db0ff2). L'estrazione è semantica con verifica a lettura
diretta: nessun dato entra per sola ricerca semantica senza lettura del contesto.

## 2.3 Curve EIOPA EUR 2020-2026

Fonte: EIOPA Risk-Free Rate Term Structures, 13 file (20200811 → 20260630). Estrazione
programmatica: fogli RFR_spot_no_VA / RFR_spot_with_VA, colonna Euro (3ª), 20 scadenze
annuali, gestione notazione scientifica e paginazione. Stato: **verified** per 6+ date
riferimento (2021-12-31, 2022-12-31, 2023/2024/2025/2026-01-31), 20/20 nodi per data e
sheet (rfr_curves_eur_2021_2022.csv, rfr_curves_eur_2023_2026.csv + addenda SOURCES).
Cross-validazione: il VA a 10y estratto dalle curve coincide con quello dichiarato nei
SFCR PVG (3 bps al 31.12.2021 [O SFCR], 19 bps al 31.12.2022).

Nota di qualità documentata: i metadati dei file 2025/2026 riportano una data errata
("2021-11-15"); la data effettiva è verificata nel foglio Main_Menu di ciascun file
(31-01-2025, 31-01-2026) e registrata nell'addendum.

## 2.4 La disciplina del n.d.

Tre casi paradigmatici: (i) ratio ISV 2020-21 da OCR corrotto ("2095") — n.d. definitivo;
(ii) residuo PV_SOLO 2022 (−6.065k) — componente "TP as a whole", annotato senza
ripartizione inventata; (iii) spread BTP-Bund 2024-2026 — assente dalle fonti [O] in
corpus, quindi n.d. e il motore lapse applica il floor (proiezione d'isteresi dichiarata
come tale, non interpolazione). La disciplina del n.d. è ciò che rende falsificabile
ogni affermazione: il lettore può sempre verificare cosa non sappiamo.

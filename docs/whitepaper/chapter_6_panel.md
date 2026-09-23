# Capitolo 6 — Il pannello cross-company

## 6.1 Stesso shock, direzioni opposte

L'argomento più robusto contro ogni lettura "da caso singolo" viene dal pannello. A parità
di shock di mercato (+307bps, VA EUR 19 bps al 31.12.2022), l'impatto sul ratio di
solvibilità è di segno opposto tra compagnie: Poste Vita Group −32,2pp contro Arca Vita
+20,5pp [O SFCR]. Una dinamica che un modello a shock uniforme non può generare per
costruzione: se lo shock è lo stesso, l'impatto può differire solo per struttura — mix
attivo (concentrazione BTP 97% in PVG al 2021 [O]), duration delle passività, presenza di
DPHB interno, regime di rivalutazione.

Arca stessa, nel SFCR 2022, attribuisce l'aumento del rischio riscatto (+63.179 k€) "al
congiunto dell'esposizione al rialzo delle frequenze di riscatto e del forte aumento dei
tassi" [O-text]: la compagnia cioè descrive in prima persona la state-dependence che il
motore dinamico formalizza.

## 6.2 Serie storica ed entity panel

Il dataset copre: serie PVG 2019-2024 (company_sfcr), entity panel PV solo / Poste Assicura /
Net Insurance per anno (entity_panel_2019_2024), e pannello 6 compagnie × motori
(cross_company_panel). L'attribuzione è stata corretta in corsa (committ v2): i dati
EOF 371.389 / SCR 158.321 / ratio 234,58% appartengono a Poste Assicura, non a Net
Insurance — errore di attribuzione tipico dei pannelli ed evitato dalla tracciabilità
a documento.

Il regime lapse differenziato per entità (models/lapse_params.md) riflette il pannello:
riscatto endogeno rilevante per LIFE_TRAD, nullo per il non-life di Poste Assicura,
trascurabile per INDEX_UL e GROUP_DIV.

## 6.3 Generalizzazione

Il risultato centrale del pannello è una proposizione controfattuale: dato lo stesso
shock, la direzione dell'impatto è una funzione della struttura (asset mix, duration,
DPHB), non dello shock. Ne segue che nessun coefficiente di sensibilità "di settore" è
stimabile senza modellare la struttura — e che ogni stress test uniforme (shift unico su
tutte le compagnie) produce errori di segno per costruzione. È la confutazione empirica
della prassi di settore standard.

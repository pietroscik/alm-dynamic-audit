# Parametri lapse (riscatto) differenziati per modello di business — [E-model]

STATO: ipotesi di modellazione, NON dati [O]. Da calibrare su dati di portafoglio.
Qui si formalizza la distinzione per ramo che evita di applicare stress comportamentali
a business che non li subiscono.

## Taxonomia dei regimi di riscatto

| Regime | Compagnie nel campione | Motivazione [O-evidence] |
|---|---|---|
| LIFE_TRADIZIONALE (lapse dinamico endogeno) | PV_GROUP, PV_SOLO, Arca Vita | DPHB massiccio (SFCR 2022: life UW +615 mln via DPHB; Arca 2025: SCR +34,7 mln "da aumento rischio riscatto" [O-text]) |
| NON_LIFE (lapse ~ 0) | Poste Assicura, Net Insurance | Ramo danni: nessuna componente discretionary benefit; SCR life UW = 0 (S.25.01.21 PA 2021 [O]) |
| INDEX/UNIT_LINKED (lapse neutrale ai tassi) | componenti PVG/ISV ramo III | Passivo non-garantito: il riscatto non genera disinvestimento forzato |
| GROUP_DIVERSIFICATO (media pesata) | ISV Group, ISPA Group | mix vita+danni: peso per TP delle due componenti (da S.12.01) |

## Parametri proposta per il motore dinamico

funzione: L(r) = L_base + gamma x max(0, r - r_bar)  con cap L_max

| Regime | L_base | gamma (elasticita' riscatto) | L_max | Note |
|---|---|---|---|---|
| LIFE_TRADIZIONALE | 5-8% p.a. | 1,5-2,5 (alto) | 25-30% | calibrare su PVG: beta del rapporto DPHB/BE |
| NON_LIFE | 0 | 0 | 0 | niente stress comportamentale |
| INDEX_UL | 3-5% p.a. | 0,5 (basso) | 15% | riscatto guidato da performance, non dai tassi |
| GROUP_DIVERSIF. | peso TP | media pesata | media pesata | = somma componenti con i rispettivi parametri |

## Evidenze di supporto nel dataset [O]
- PVG 2022: SCR life UW 13.469.741 lordo (rischio riscatto parte del modulo) con LAC TP -11.299.794: il
  riscatto e' il driver dominante del +615 mln di SCR
- Arca Vita 2025 [O-text]: SCR +34.676 "principalmente dall'aumento dei Rischi Tecnico Assicurativi
  Vita determinato dall'incremento del rischio riscatto... rialzo della curva dei tassi congiuntamente
  all'esposizione a frequenze di riscatto" — conferma empirica del legame tassi->riscatto nel campione
- PA 2021 [O]: S.25.01.21 senza voce life underwriting risk — conferma lapse=0 per danni

# Stabilità di gamma (DPHB lapse) su finestra estesa 2019-2023 — PVG

**Tag: [E-model] su input [O]/[O-text]/[E-derived] tracciati in data/interim/lapse_flows_pvg_ext.csv.**

## 1. Nuovi dati estratti (2023 e 2019-2020)

- SFCR PVG 2023 (doc 82db0ff2), Exec summary: frequenza riscatti su riserve medie **4,4% (2023) vs 3,5% (2022)**;
  lapses **+1,7 mld** vs 2022; riferimento di mercato **10,6%** (Ania Trends n.4/2024).
- SFCR PVG 2020 (doc ca788307): riscatti 2020 **3,2 mld**, **-0,3 mld** vs 2019 (→ 2019 = 3,5 mld [E-derived]).
- Spread BTP-Bund fine anno [O-text Arca 2022/2023]: 2021 ~135 bps, 2022 211 (alt. 214), 2023 **166**.

## 2. Test di stabilità di gamma

| Transizione | Misura | Δs (bps) | m osservato | gamma implicito |
|---|---|---|---|---|
| 2021→2022 | ratio su riserve aperture (3,1→3,6) | +76 | 1,161 | **+19,7** |
| 2022→2023 | frequenza su riserve medie (3,5→4,4) | -45 (anno civile) | 1,257 | **-47,7 (contemporaneo)** |
| 2022→2023 | specificazione lag-1 (risposta 2023 allo shock 2022) | +76 | 1,257 | **+30,1** |

## 3. Letture

1. La specificazione contemporanea q(s)=q0*exp(gamma*ds) è **rigettata out-of-sample nel 2023**:
   lo spread scende (214→166) ma i riscatti salgono (3,5%→4,4%). Un modello statico o lineare
   non può riprodurre questa dissociazione.
2. La specificazione **lag-1** ripristina la coerenza: gamma_lag = 30,1 cade esattamente nella banda
   stimata sul biennio 2021-22 [19,7 – 30,2] (upper bound). Il comportamento non è istantaneo:
   l'elasticità agisce con un anno di ritardo (inerzia contrattuale/distributiva del portafoglio postale).
3. Conferma direzionale 2019-2020: riscatti in calo (3,5→3,2 mld) nel regime di tassi ultra-bassi
   [O-text]; gamma non calcolabile per mancanza di spread [O] 2019-2020 (resta n.d., mai interpolato).
4. Il gap verso il mercato (4,4% vs 10,6% Ania 2023) conferma che PVG è il caso conservativo:
   anche con gamma>0 il portafoglio postale riscatta meno della media di mercato.

## 4. Specificazione raccomandata per il motore dinamico

    q_t = q0 * exp(gamma * max(0, ds_{t-1}))     con gamma in [19,7; 30,1], centrale 19,7
    (floor a 0: risposta asimmetrica - il narrowing non riduce i riscatti sotto la base)

La forma asimmetrica (floor) spiega sia il 2022 (shock → riscatti su) sia il 2023 (narrowing →
riscatti NON scendono: isteresi comportamentale). E' esattamente la state-dependence che il
motore statico non può catturare.

## 5. Regime nel data dictionary

LIFE_TRAD (PVG): gamma = 19,7 central, banda [19,7; 30,1], lag = 1 anno, floor attivo.
INDEX_UL / NON_LIFE / GROUP_DIV: gamma non applicabile (riscatto endogeno trascurabile).

# Specifica Matematica: ALM Dynamic Audit Engine (v1.0)

## 1. Obiettivo e notazione
Il framework confronta una metrica di solvibilita' statica (approccio
lineare tradizionale) con una metrica dinamica (mark-to-market con lapse
endogeno) per calcolare il Delta "Blind Spot".

Notazione di base:
- t appartenente a {1, ..., T}: orizzonte temporale in anni (MVP: T=10)
- r_t: tasso risk-free (EIOPA) al tempo t
- s_t: spread sovrano applicato agli attivi al tempo t
- CF_t^A, CF_t^L: cash flow di attivi e passivi (baseline)
- L_t: tasso di riscatto (lapse rate) al tempo t

## 2. Tasso di riscatto endogeno (lapse function)
L_t = min( L_max, L_base + gamma * max(0, r_mkt - r_port - c_fric) )

dove:
- r_mkt: tasso di mercato di riferimento percepito (BTP breve),
  coerente con la curva shockata
- r_port: rendimento medio retrocesso dal portafoglio
- gamma: sensibilita' comportamentale allo spread di rendimento [E]
- c_fric: frizione / penale di riscatto

## 3. Rimodellazione dei flussi passivi
I flussi CF_t^L vengono deformati se L > L_base: una quota pro-quota
dei flussi futuri e' anticipata (front-loading) verso gli anni
precedenti, conservando il totale nominale. Implementazione in
cashflow_builder.reshape_with_lapse.

## 4. Motore statico (benchmark lineare)
Sia dr_par lo shift parallelo equivalente della curva.
- A_stat   = A_0   * (1 - D_mod^A * dr_par)
- BEL_stat = BEL_0 * (1 - D_mod^L * dr_par)
- OF_stat  = A_stat - BEL_stat

## 5. Motore dinamico e liquidity engine
- A_dyn   = somma su t di CF_t^A / (1 + r_t + s_t)^t
  (s_t applicato solo alla quota sovrana di ogni nodo)
- BEL_dyn = somma su t di CF~_t^L / (1 + r_t)^t
  (flussi rimodellati dal lapse, sconto risk-free)

Fabbisogno di liquidita' e fire sales (finestra anno 1):
- Shortfall_1 = max(0, CF~_1^L - CF_1^A - B_0)
- V_sell      = Shortfall_1 * (1 + h)
- C_liq       = V_sell - Shortfall_1 = Shortfall_1 * h

- OF_dyn = A_dyn - BEL_dyn - C_liq

## 6. Output: Delta Blind Spot
Delta_blind_spot = OF_stat - OF_dyn

## 7. Test di coerenza minimi (sanity checks)
1. Se gamma = 0 e s_t = 0, statico e dinamico convergono (a meno della
   pura convessita').
2. Se gamma > 0 e i tassi salgono, la duration passiva dinamica e'
   strettamente minore di quella statica.
3. Se Shortfall_1 > 0 e h > 0, allora C_liq > 0.
4. dr > 0 => il PV di un portafoglio obbligazionario lungo scende.
5. reshape con lapse = base => flussi invariati (identita').

## 8. Assunzioni e limitazioni dichiarate
- Flussi sintetici: approssimano il profilo temporale compatibile con
  duration e aggregati osservabili; NON replicano il portafoglio reale.
- Curva a nodi annui (MVP); finestra di liquidita' annua.
- Lapse a un fattore; gamma e haircut sono [E] non calibrati:
  sensitivity analysis obbligatoria prima di conclusioni quantitative.
- La copertura riassicurativa del mass lapse (dove dichiarata, es.
  Poste Vita) mitiga parte del blind spot: i risultati sono un upper bound.

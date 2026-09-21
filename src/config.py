"""Parametri di configurazione del motore.

TUTTI i parametri comportamentali sono [E] Estimated: assunzioni
dichiarate con razionale, da esplorare con sensitivity analysis.
Nessuno di questi valori e' un dato osservato.
"""

from __future__ import annotations

# --- comportamento di riscatto (lapse) ---
LAPSE_BASE = 0.045
# Tasso annuo di riscatto fisiologico pre-shock.
# Razionale: media storica portafogli rivalutabili italiani (IVASS).

LAPSE_GAMMA = 0.35
# Sensibilita' dinamica: dLapse = gamma * max(0, r_mkt - r_port - c_fric).
# Razionale: calibrazione da letteratura sui lapse; DA ESPLORARE con
# sensitivity analysis (es. gamma in [0, 1.5]).

LAPSE_MAX = 0.40
# Cap del tasso di riscatto (saturazione comportamentale).

R_MKT = 0.045     # rendimento alternativo percepito (BTP breve)
R_PORT = 0.010    # rendimento retrocesso dal portafoglio
C_FRIC = 0.010    # frizione / penale di riscatto

# --- liquidazione forzata (fire sales) ---
HAIRCUT = 0.15
# Penalizzazione di smobilizzo forzoso per coprire la liquidita'.
# Razionale: haircut prudenziale da stress test di liquidita'.
# NOTA: haircut sui governativi in assenza di default sovrano = 0
# (trattamento Solvency II Standard Formula); l'haircut si applica
# al costo di smobilizzo rapido, non al merito di credito.

# --- costruzione cash flow sintetici ---
BASE_RATE = 0.02     # tasso base per i profili sintetici
TENOR = 10           # orizzonte in anni (MVP)

# --- pesi SPS (dichiarati [E], soggetti a revisione) ---
SPS_WEIGHTS = {"delta": 0.5, "liq": 0.3, "solv": 0.2}

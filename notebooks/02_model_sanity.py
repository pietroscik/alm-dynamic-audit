# Notebook 2 - Model Sanity Check
# Prova le formule su casi sintetici SEMPLICI con soluzione nota a mano,
# e visualizza curva, PV, duration, convexity.
# Obiettivo: validare la matematica PRIMA di applicarla ai dati reali.
# Deve girare dopo il Notebook 1 e prima del Notebook 3.

# %%
import numpy as np
import polars as pl
import matplotlib.pyplot as plt

from src.metrics import (
    present_value, macaulay_duration, modified_duration, convexity,
    parallel_shift,
)
from src.cashflow_builder import (
    build_liability_cashflows, build_asset_cashflows, reshape_with_lapse,
    _fit_profile_exponent,
)
from src.dynamic_engine import calculate_lapse_rate

plt.rcParams["figure.figsize"] = (10, 4)
np.set_printoptions(precision=4, suppress=True)

# %% [markdown]
# # Caso 1 - Zero-coupon: soluzione analitica nota
# Un flusso unico di 100 all'anno 10, tasso 2%:
# PV = 100 / 1.02^10, duration Macaulay = 10, convexity nota.

# %%
cf_zc = np.zeros(10); cf_zc[9] = 100.0
r = 0.02
pv_expected = 100.0 / 1.02**10
pv_actual = present_value(cf_zc, r)
dur_actual = macaulay_duration(cf_zc, r)
conv_actual = convexity(cf_zc, r)
# convexity teorica di uno ZC: t(t+1)/(1+r)^2
conv_expected = 10 * 11 / (1 + r) ** 2

print(f"PV:    atteso {pv_expected:.6f}  ottenuto {pv_actual:.6f}")
print(f"Dur:   atteso 10.000000  ottenuto {dur_actual:.6f}")
print(f"Conv:  atteso {conv_expected:.6f}  ottenuto {conv_actual:.6f}")
assert abs(pv_actual - pv_expected) < 1e-9
assert abs(dur_actual - 10.0) < 1e-9
assert abs(conv_actual - conv_expected) < 1e-9
print("CASO 1: PASS")

# %% [markdown]
# # Caso 2 - Due flussi equamente pesati: barbell semplice

# %%
cf_bb = np.zeros(10); cf_bb[0] = 50.0; cf_bb[9] = 50.0
t = np.arange(1, 11)
manual_dur = np.sum(t * cf_bb / 1.02**t) / np.sum(cf_bb / 1.02**t)
print(f"Duration manuale {manual_dur:.6f} vs calcolata "
      f"{macaulay_duration(cf_bb, 0.02):.6f}")
assert abs(manual_dur - macaulay_duration(cf_bb, 0.02)) < 1e-12
assert 1 < manual_dur < 10
print("CASO 2: PASS")

# %% [markdown]
# # Caso 3 - Relazione duration/PV: il grafico di sensibilita'
# La tangente in r=0.02 e' la modified duration: verifica grafica
# della formula lineare usata dallo static engine.

# %%
cf_long = build_liability_cashflows(48000.0, 8.8, tenor=10,
                                    base_rate=0.02)["cashflow"].to_numpy()
cf_short = build_liability_cashflows(48000.0, 3.0, tenor=10,
                                     base_rate=0.02)["cashflow"].to_numpy()

rates = np.linspace(0.00, 0.06, 25)
pv_long = [present_value(cf_long, x) for x in rates]
pv_short = [present_value(cf_short, x) for x in rates]

d_mod = modified_duration(cf_long, 0.02)
pv0 = present_value(cf_long, 0.02)
tangent = pv0 * (1 - d_mod * (rates - 0.02))

fig, ax = plt.subplots()
ax.plot(rates, pv_long, label="PV esatto (lungo, D=8.8)")
ax.plot(rates, pv_short, label="PV esatto (corto, D=3.0)")
ax.plot(rates, tangent, "--", label="Approssimazione statica (1 ordine)")
ax.set_xlabel("tasso r"); ax.set_ylabel("PV (mln)")
ax.legend(); ax.set_title("Sensibilita' ai tassi: esatto vs lineare")
plt.show()

err_near = abs(pv0 * (1 - d_mod * 0.005) - present_value(cf_long, 0.025))
err_far = abs(pv0 * (1 - d_mod * 0.03) - present_value(cf_long, 0.05))
print(f"Errore lineare @ +50bps: {err_near:.1f}  |  @ +300bps: {err_far:.1f}")
assert err_far > err_near * 10
print("CASO 3: PASS (il gap di convessita' cresce con lo shock)")

# %% [markdown]
# # Caso 4 - Profilo dei cash flow sintetici: duration target

# %%
fig, axes = plt.subplots(1, 2, figsize=(12, 4))
for target in (3.0, 5.5, 8.8):
    cf = build_liability_cashflows(48000.0, target, tenor=10,
                                   base_rate=0.02)["cashflow"].to_numpy()
    achieved = macaulay_duration(cf, 0.02)
    axes[0].plot(range(1, 11), cf, marker="o", label=f"target {target}")
    print(f"target duration {target:.1f} -> achieved {achieved:.3f}")
    assert abs(achieved - target) < 0.15
axes[0].set_title("Profili passivi sintetici per duration target")
axes[0].set_xlabel("bucket year"); axes[0].legend()

ks = np.linspace(0, 12, 25)
durs = []
w = np.arange(1, 11)
for k in ks:
    ww = w**k
    durs.append(macaulay_duration(ww / ww.sum() * 100, 0.02))
axes[1].plot(ks, durs)
axes[1].set_xlabel("esponente k"); axes[1].set_ylabel("duration")
axes[1].set_title("Monotonia k -> duration")
plt.show()
durs_arr = np.array(durs)
assert np.all(np.diff(durs_arr) > -1e-9), "la duration deve crescere con k"
print("CASO 4: PASS")

# %% [markdown]
# # Caso 5 - Lapse function: forma e cap

# %%
gammas = np.linspace(0, 1.5, 40)
r_mkt_grid = [0.03, 0.045, 0.06]
fig, ax = plt.subplots()
for r_mkt in r_mkt_grid:
    lapses = [calculate_lapse_rate(0.05, r_mkt, 0.01, g) for g in gammas]
    ax.plot(gammas, lapses, label=f"r_mkt={r_mkt:.3f}")
ax.axhline(0.40, color="grey", ls=":", label="L_max")
ax.set_xlabel("gamma"); ax.set_ylabel("lapse rate")
ax.set_title("Lapse endogeno: min(L_max, L_base + g*max(0, incentivo))")
ax.legend(); plt.show()

assert calculate_lapse_rate(0.05, 0.005, 0.01, 0.5) == 0.05
l_low = calculate_lapse_rate(0.05, 0.045, 0.01, 0.10)
l_high = calculate_lapse_rate(0.05, 0.045, 0.01, 0.20)
assert abs((l_high - 0.05) - 2 * (l_low - 0.05)) < 1e-12
print("CASO 5: PASS")

# %% [markdown]
# # Caso 6 - Reshaping dei flussi: conservazione del nominale

# %%
cf_base = build_liability_cashflows(48000.0, 8.8, tenor=10,
                                    base_rate=0.02)["cashflow"]
df = pl.DataFrame({"bucket_year": range(1, 11),
                   "cashflow": cf_base.to_numpy()})
cf_stress = reshape_with_lapse(df, 0.30)["cashflow"].to_numpy()

fig, ax = plt.subplots()
x = np.arange(1, 11)
ax.bar(x - 0.2, cf_base.to_numpy(), width=0.4, label="base (lapse 5%)")
ax.bar(x + 0.2, cf_stress, width=0.4, label="stress (lapse 30%)")
ax.set_xlabel("bucket year"); ax.set_ylabel("flusso (mln)")
ax.set_title("Front-loading dei flussi passivi")
ax.legend(); plt.show()

assert abs(cf_base.sum() - cf_stress.sum()) < 1e-6, "nominale conservato"
print(f"CASO 6: PASS (totale nominale {cf_base.sum():.1f} conservato)")

# %% [markdown]
# # Caso 7 - Curva EIOPA e shift parallelo

# %%
curve_base = np.array([0.0125, 0.0160, 0.0185, 0.0200, 0.0210,
                       0.0218, 0.0225, 0.0231, 0.0236, 0.0240])
curve_up = parallel_shift(curve_base, 250.0)   # +250 bps
curve_dyn = curve_up + 0.35 * 0.0230           # + spread sulla quota sovrana

fig, ax = plt.subplots()
ax.plot(range(1, 11), curve_base * 100, marker="o", label="EIOPA base")
ax.plot(range(1, 11), curve_up * 100, marker="s", label="+250bps parallelo")
ax.plot(range(1, 11), curve_dyn * 100, marker="^",
        label="dinamica: +250bps + 35% quota spread 230bps")
ax.set_xlabel("scadenza (anni)"); ax.set_ylabel("tasso (%)")
ax.set_title("Curve di sconto: statico vs dinamico")
ax.legend(); plt.show()

np.testing.assert_allclose(curve_up - curve_base, np.full(10, 0.025))
print("CASO 7: PASS")

# %% [markdown]
# ## Esito complessivo
# Tutti i 7 casi sintetici devono dare PASS. Solo a quel punto il codice
# e' promuovibile al Notebook 3 (historical replay) e infine alla dashboard.

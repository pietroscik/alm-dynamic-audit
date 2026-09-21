# Notebook 1 - Data Audit
# Verifica completezza, fonti e classificazione O/D/E
# prima di far girare qualunque motore.
# Esecuzione: jupyter nbconvert o direttamente python notebooks/01_data_audit.py
# (struttura "percent-style" compatibile con jupytext).

# %%
from pathlib import Path

import polars as pl

from src.data_loader import load_all
from src.data_quality import run_quality_checks

pl.Config.set_tbl_cols(30)
pl.Config.set_tbl_width_chars(200)

PROCESSED = Path("data/processed")

# %% [markdown]
# # 1. Caricamento delle tre tabelle del MVP

# %%
tables = load_all(PROCESSED)
company = tables["company_sfcr"]
macro = tables["macro_series"]
scenarios = tables["stress_scenarios"]

# %% [markdown]
# # 2. Shape, null count, campi mancanti

# %%
for name, df in tables.items():
    print(f"\n=== {name} ===")
    print(f"shape: {df.shape}")
    if df.height:
        nulls = df.null_count().transpose(include_header=True)
        nulls.columns = ["column", "nulls"]
        print(nulls.filter(pl.col("nulls") > 0) if nulls.height else "nessun nullo")
        print(df.head(5))

# %% [markdown]
# # 3. Data quality report (ERROR blocca, WARN segnala)

# %%
report = run_quality_checks(tables)
print(report.summary())
for v in report.violations:
    print(f"[{v.severity:5s}] {v.table}.{v.column}: {v.message}")
assert not report.has_errors, "Risolvere gli ERROR prima di procedere."

# %% [markdown]
# # 4. Copertura compagnie-anni

# %%
if company.height:
    coverage = (company
                .group_by("company_id")
                .agg(pl.col("report_date").min().alias("from"),
                     pl.col("report_date").max().alias("to"),
                     pl.len().alias("n_reports"))
                .sort("company_id"))
    print(coverage)

# %% [markdown]
# # 5. Tabella di classificazione O/D/E (dal data_dictionary.csv)

# %%
dd_path = Path("data_dictionary.csv")
if dd_path.exists():
    dd = pl.read_csv(dd_path)
    print(dd.group_by("O_D_E").len())
    print(dd.select("field", "table", "O_D_E", "source"))
else:
    print("data_dictionary.csv non trovato: creare prima del primo audit.")

# %% [markdown]
# # 6. Scenari disponibili

# %%
print(scenarios)

# %% [markdown]
# ## Checklist di uscita
# - [ ] nessun ERROR nel quality report
# - [ ] WARN esaminati e giustificati
# - [ ] ogni compagnia ha almeno 2 report annui
# - [ ] data_dictionary.csv presente e coerente con le colonne caricate

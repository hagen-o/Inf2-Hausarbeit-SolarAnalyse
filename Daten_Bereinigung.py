import pandas as pd
from pathlib import Path
import numpy as np

# Konfiguration
DATA_DIR = Path(r"C:\Users\Hagen\OneDrive\HKA\WS25-26\Informatik2\Matthias\Hausarbeit\Inf2-Hausarbeit-SolarAnalyse\Rohdaten")
FILES = [
    "26_measurements.csv",
    "27_measurements.csv",
    "28_measurements.csv",
]

# Metadaten: kWp = Kilowatt peak
#              W = kWp * 1000
# MAX_POWER_W = kWp × 1000 × Sicherheitsfaktor(1.1)
# Notwendig um einzelne Ausreiser herauszufiltern
MAX_POWER_BY_FILE = {
    "26_measurements.csv": 8200,
    "27_measurements.csv": 13000,
    "28_measurements.csv": 10200,
}

def clean_pv_measurements(csv_path: Path, max_power_w: float) -> pd.DataFrame:
    # CSV einlesen
    df = pd.read_csv(csv_path, sep=";")

    # PV-Leistungsspalte finden
    # iteriert über alle Spalten und sucht Teilstring "pv_power"
    power_candidates = [c for c in df.columns if "pv_power" in c]
    if not power_candidates:
        raise ValueError(f"Keine pv_power-Spalte gefunden in: {csv_path.name}")
    power_col = power_candidates[0]

    # Dezimal-Komma wird zu . umgewandelt, dann als zu float geändert
    df[power_col] = (
        df[power_col]
        .astype(str)
        .str.replace(",", ".", regex=False)
        .astype(float)
    )

    # Zeitstempel aus t_local werden in UTC Format überführt
    df["timestamp"] = pd.to_datetime(df["t_local"], utc=True)

    # Aufräumen: redundante Spalten weg, sortieren
    # t_unix & t_local entfernen und durch timestamp ersetzen
    # neuer Index für timtestamp
    df = (
        df.drop(columns=["t_local", "t_unix"], errors="ignore")
          .sort_values("timestamp")
          .reset_index(drop=True)
    )

    # Neue Spalte interval_minutes, gibt Zeitlichen Abstand zur vorherigen Zeile in min an
    df["interval_minutes"] = df["timestamp"].diff().dt.total_seconds() / 60

    # Plausibilisierung: negativ -> 0, zu groß -> NaN
    df.loc[df[power_col] < 0, power_col] = 0
    df.loc[df[power_col] > max_power_w, power_col] = np.nan

    # Tag/Nacht-Kennzeichen
    df["is_generation"] = df[power_col] > 0

    # Fehlende Werte (nur kurze Lücken) interpolieren
    df[power_col] = df[power_col].interpolate(limit=2)

    # Einheitliche Benennung
    df = df.rename(columns={power_col: "pv_power_w"})

    # Zeitfeatures
    df["hour"] = df["timestamp"].dt.hour
    df["day"] = df["timestamp"].dt.date
    df["month"] = df["timestamp"].dt.month
    df["weekday"] = df["timestamp"].dt.weekday

    # Energie (kWh): W * Minuten -> Wh -> kWh
    df["pv_energy_kwh"] = df["pv_power_w"] * (df["interval_minutes"] / 60) / 1000

    return df

# Sicherheitscheck: Pfad-Check
for f in FILES:
    full_path = DATA_DIR / f
    if not full_path.exists():
        raise FileNotFoundError(f"Datei nicht gefunden: {full_path}")

# Alle Dateien bereinigen
cleaned_data = {}

for file in FILES:
    path = DATA_DIR / file
    max_power = MAX_POWER_BY_FILE[file]
    cleaned_data[file] = clean_pv_measurements(path, max_power)

# Zusammenführen
df_all = pd.concat(
    cleaned_data.values(),
    keys=cleaned_data.keys(),
    names=["source_file", "row"]
).reset_index(level="source_file")

# Checks
print(df_all.info())
print(df_all.describe())

# bereinigte Daten speichern
OUT_DIR = Path("Bereinigt")
OUT_DIR.mkdir(exist_ok=True)

for filename, df in cleaned_data.items():
    out_path = OUT_DIR / f"cleaned_{filename}"
    df.to_csv(out_path, index=False)
    print(f"Gespeichert: {out_path}")
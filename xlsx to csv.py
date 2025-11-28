import pandas as pd
from pathlib import Path

# excel Dateien zu csv umwandeln
ordner_ursprung = Path(r"C:\Users\Hagen\OneDrive\HKA\WS25-26\Informatik2\Matthias\Hausarbeit\Inf2-Hausarbeit-SolarAnalyse\Rohdaten monatlicher Report 22-25")
ordner_ziel = Path(r"C:\Users\Hagen\OneDrive\HKA\WS25-26\Informatik2\Matthias\Hausarbeit\Inf2-Hausarbeit-SolarAnalyse\Daten als CSV")

for excel_datei in ordner_ursprung.glob("*.xlsx"):
    df = pd.read_excel(excel_datei)
    csv_datei = ordner_ziel / (excel_datei.stem + ".csv") # entfernt Dateiendung .xlsx und ersetzt durch .csv
    df.to_csv(csv_datei, index=False)
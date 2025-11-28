import pandas as pd

# zeigt erste excel Datei an
df = pd.DataFrame(pd.read_excel(r"C:\Users\Hagen\OneDrive\HKA\WS25-26\Informatik2\Matthias\Hausarbeit\Inf2-Hausarbeit-SolarAnalyse\Rohdaten monatlicher Report 22-25\Solar_Monatlicher_Report_2022_04.xlsx"))
print(df)

# zeigt erste csv Datei an
df2 = pd.DataFrame(pd.read_csv(r"C:\Users\Hagen\OneDrive\HKA\WS25-26\Informatik2\Matthias\Hausarbeit\Inf2-Hausarbeit-SolarAnalyse\Daten als CSV\Solar_Monatlicher_Report_2022_04.csv"))
print(df2)
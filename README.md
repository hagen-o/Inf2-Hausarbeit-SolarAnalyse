## Rohdaten
Drei CSV Dateien mit Daten über die jeweilige PV-Anlage.

- **t_local**
  Zeitstempel(UTC), jeweils auf volle Stunde gerundet

- **t_unix**
  Anzahl der Sekunden, welche seit dem 01.01.1970, 00:00:00 UTC vergangen sind.

- **ems_28_pv_power_supply_w**
  Momentane Einspeisung der PV-Anlage in Watt



## Metadaten

Zu jeder PV-Anlage existiert eine separate Metadaten-Datei.  
Diese enthält **statische Informationen**, die sich nicht zeitlich ändern und für die
Interpretation der Rohdaten notwendig sind.

- **Inbetriebnahmejahr**  
  Jahr (ggf. Monat) der Inbetriebnahme der PV-Anlage. Relevant für
  Einspeisevergütung und regulatorische Einordnung.

- **Installierte Leistung (kWp)**  
  Nennleistung der Anlage unter Standard-Testbedingungen (STC).
  Dient als Referenz für Ertragsvergleiche.

- **Einspeisevergütung (ct/kWh)**  
  Vergütungssatz gemäß EEG(Erneuerbare-Energien-Gesetz) zum Zeitpunkt der Inbetriebnahme.

- **Ausrichtung (Azimut)**  
  Himmelsrichtung der Module relativ zu Süden.
  Negative Werte entsprechen Ost-, positive Westabweichungen.

- **Neigung (Tilt)**  
  Neigungswinkel der Module relativ zur Horizontalen in Grad.

- **Wechselrichter**  
  Angaben zu Typ und Anzahl der eingesetzten Wechselrichter.
  Relevant für mögliche Leistungsbegrenzungen (Clipping).

- **Standort (Latitude, Longitude)**  
  Geografische Koordinaten der Anlage im WGS84-Referenzsystem.
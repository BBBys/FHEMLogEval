# FHEMLogEval
Evaluate Logs produced by FHEM Home Automation
# Ablaufschritte 
## erforderlich
Samba-Freigabe der Logfiles auf dem Server
## 00Sammeln
- Logfile-Verzeichnis vom Server einhängen
  - Mountpoint ist auf /tmp
- für jedes Logfile einen Eintrag in die Datenbank machen
  - Name
  - Format der Einträge
## 10Auswertung
für jeden Eintrag in der Datenbank eine Übersicht erstellen
- Zeitraum
- Anzahl der Meldungen
- fehlerhafte Meldungen
- Messstellen
## 11Auswertung
Logfiles durchsuchen und Informationen über Messungen ausgeben.
- Zeitraum
- Anzahl der Meldungen
- fehlerhafte Meldungen
- Messstellen
Macht also das gleiche, aber ohne Datenbank zu bentzen
## wiederholt verwendete Parameter
* -k: eingehängtes Verzeichnis bleibt erhalten
* -v: wie üblich: Debug-Ausgabe
## FLElib
... fasst zentrale Module zusammen
# Lizenz
FHEM Logs Evaluator  © 2025 by Dr. Burkhard Borys 
is licensed under CC BY-NC-ND 4.0. 
To view a copy of this license, visit 
https://creativecommons.org/licenses/by-nc-nd/4.0/
# Quellen
https://pythonguides.com/check-if-a-string-is-a-valid-date-in-python/
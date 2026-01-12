# FHEMLogEval

Evaluate Logs produced by FHEM Home Automation.

# Ablaufschritte 

## erforderlich

Zugriff auf die Logfiles (/opt/fhem/log/*), direkt oder mit Samba-Freigabe der Logfiles auf dem Server.

## 00Sammeln

- Logfile-Verzeichnis vom Server einhängen
  - Mountpoint ist auf /tmp
- für jedes Logfile einen Eintrag in die Datenbank machen
  - Name
  - Format der Einträge

## 10Auswertung :unamused::unamused::unamused: Fehlschlag

Für jeden Eintrag in der Datenbank eine Übersicht erstellen
- Zeitraum
- Anzahl der Meldungen
- fehlerhafte Meldungen
- Messstellen

## 11Auswertung

Log-Files, die im angegebenen Verzeichnis liegen 
grob auswerten und zu jedem eine Übersicht ausgeben.
Falls im angegebenen Verzeichnis nicht die FHEM-Logfiles liegen,
was an der Datei ```fhem.save``` erkannt wird,
wird dieses Verzeichnis vom FHEM-Server gemounted.

Ausgegeben wird
- Zeitraum
- Anzahl der Meldungen
- fehlerhafte Meldungen
- Messstellen

Macht also das gleiche wie 10Auswertung, aber ohne eine Datenbank zu benutzen.

Das Modul ist so aufgebaut, dass es automatisch periodisch ablaufen kann - etwa in cron.daily, ...weekly oder ...monthly.

## 20Erfassen

Log-Files durchsuchen und Messwerte in eine Datenbank 
schreiben, von wo aus sie sortiert und weiterverarbetet werden können.

Wahlweise DB löschen und neu erfassen oder vorhandene Einträge
mit neuen Daten erweitern.

Verwendung von pfad: 
1) kein Pfad: nur Aufräum-Aktionen in der Datenbank.
2) Pfad enthält ein oder mehr Logfiles: diese auswerten
3) Pfad ist leer: FHEM-Log-Verzeichnis vom Server laden und auswerten

Die Datenbank wird bei jedem Lauf bereinigt, indem doppelte und irrelevante 
Einträge gelöscht werden.

## 50Plots - Sackgasse :unamused:

Sollte mal Daten grafisch darstellen. Jetzt weitergeführt als 52Plots

Liest die Daten aus einer CSV-Datei, die vorher aus der Datenbank durch 
Export erzeugt werden muss.

## 52Plots

Stellt Daten grafisch dar.

Liest die Daten direkt mit Pandas aus der Datenbank.

## wiederholt verwendete Parameter

* -k: eingehängtes Verzeichnis bleibt erhalten
* -v: wie üblich: Debug-Ausgabe

## FLElib

... fasst zentrale Module zusammen
Einbinden mit ```export PYTHONPATH="../FLElib"```

### mountlogs
#### mountLogs / unmountLogs
Mounted Log-Verzeichnis vom 🖥 FHEM-Server.
Verwendung:

```
from mountlogs import mountLogs, unmountLogs
pfadErgebnis=mountLogs(pfadVorgabe)
...
unmountLogs(logPath)
```

#### istLogDir

Test, ob das Verzeichnis Logfiles enthält

# Lizenz

FHEM Logs Evaluator  © 2025 by Dr. Burkhard Borys 
is licensed under CC BY-NC-ND 4.0. 
To view a copy of this license, visit 
https://creativecommons.org/licenses/by-nc-nd/4.0/

# Quellen

    [1] Benjamin Baka, Python data structures and algorithms : improve 
    the performance and speed of your applications. Packt Publishing, 2017.
  
    [2] Ivan Idris, Python data analysis cookbook : over 140 practical 
    recipes to help you make sense of your data with ease and build 
    production-ready data apps. Packt Publishing, 2016.
    
    [3] Alice Zheng and Amanda Casari, Feature engineering for machine
    learning : principles and techniques for data scientists. 
    O’Reilly Media, 2018.

    [4] Alberto Boschetti and Luca Massaron, Python data science essentials : 
    become an efficient data science practitioner by understanding Python’s 
    key concepts. Packt Publishing, 2016.

    [5] VS Code's Copilot.
  
  

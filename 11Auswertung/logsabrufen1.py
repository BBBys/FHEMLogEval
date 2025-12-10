# from dbparam import DBTLOGS
import sys, os  # , mysql.connector
import logging
from logauswerten1 import logAuswerten1
from loganalyse import logAnalyse
from fhemnamen import nameReduzieren


# Liste der Logfiles abrufen
# jede einzelne auswerten
def logsAbrufen1(pfad, Dbg=False):
    if not os.path.exists(pfad):
        logging.fatal(f"logsAbrufen: Pfad {pfad} existiert nicht.")
        return f"Pfad {pfad} existiert nicht."
    OK = False
    for root, dirs, dateien in os.walk(pfad):
        for dateiName in dateien:
            if dateiName.endswith("fhem.log"):
                continue
            if dateiName == "fhem.save":
                continue
            if dateiName == "eventTypes.txt":
                continue
            dateiMitPfad = os.path.join(root, dateiName)
            if os.path.getsize(dateiMitPfad) < 10:
                logging.info(f"{dateiName} zu klein, übersprungen")
                continue
            # basisName = nameReduzieren(datei)
            logging.debug(f"logsAbrufen: Datei {dateiName} wird ausgewertet")
            OK = logAuswerten1(dateiName, dateiMitPfad, Dbg)
            if not OK:
                break

    return

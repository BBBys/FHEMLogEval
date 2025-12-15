# from dbparam import DBTLOGS
import sys, os  # , mysql.connector
import logging
from logauswerten1 import logAuswerten1
from loganalyse import logAnalyse
from fhemnamen import nameReduzieren


# Liste der Logfiles abrufen
# jede einzelne auswerten
def logsAbrufen1(pfad, interaktiv=False, Dbg=False):
    if not os.path.exists(pfad):
        logging.fatal(f"logsAbrufen: Pfad {pfad} existiert nicht.")
        return f"Pfad {pfad} existiert nicht."
    OK = False
    idatei = 0
    for root, dirs, dateien in os.walk(pfad):
        for dateiName in dateien:
            # diverse Dateien werden nich ausgewertet:
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
            # dann auswerten:
            idatei += 1
            logging.info(f"{idatei}.: {dateiName} wird ausgewertet")
            OK = logAuswerten1(dateiName, dateiMitPfad, Dbg)
            if interaktiv and not OK:
                break

    return

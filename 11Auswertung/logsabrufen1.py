# from dbparam import DBTLOGS
import time, os
import logging
from logauswerten1 import logAuswerten1


# Liste der Logfiles abrufen
# jede einzelne auswerten
def logsAbrufen1(pfad, interaktiv=False, Dbg=False):
    if not os.path.exists(pfad):
        logging.fatal(f"logsAbrufen: Pfad {pfad} existiert nicht.")
        return f"Pfad {pfad} existiert nicht."
    
    OK = False
    idatei = 0
    summeZeilen = 0
    startzeit = time.time()

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
            OK, nZeilen = logAuswerten1(dateiName, dateiMitPfad, Dbg)
            summeZeilen += nZeilen
            if interaktiv and not OK:
                break
            if Dbg and idatei >= 3:
                break

    stoppzeit = time.time()
    dauer = stoppzeit - startzeit
    spd = dauer / idatei
    dpz = summeZeilen / dauer
    logging.info(f"Zeit\t{dauer:.0f} s")
    logging.info(f"Dateien\t{idatei}")
    logging.info(f"Zeilen\t{summeZeilen}")
    logging.info(f"\t\t{spd:.3f}\tSekunden / Datei")
    logging.info(f"\t\t{dpz:.0f}\tZeilen / Sekunde")

    return

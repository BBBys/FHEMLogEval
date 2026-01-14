import os, logging
from verarbeiten import verarbeiten


def suchen(pfad, db, Dbg=False):
    """
    Sucht in den Log-Dateien im angegebenen Pfad nach Messwerten
    und schreibt diese in die Datenbank.
    """
    if not os.path.exists(pfad):
        logging.fatal(f"logsEintragen: Pfad {pfad} existiert nicht.")
        return 0
    for root, dirs, alleDateien in os.walk(pfad):
        iDatei = 0
        gesamtZeilen = 0
        for datei in alleDateien:
            fileMitPfad = os.path.join(root, datei)
            # Dateien ausschließen
            if datei.endswith("fhem.log"):
                continue
            if datei == "fhem.save":
                continue
            if datei == "eventTypes.txt":
                continue
            if os.path.getsize(fileMitPfad) < 10:
                continue
            iDatei += 1
            # if Dbg and iDatei > 5:
            #    break
            logging.debug(f"Verarbeite Datei: {fileMitPfad}")
            with open(fileMitPfad, "r") as f:
                nZeilen = verarbeiten(f, db, Dbg)
            gesamtZeilen += nZeilen
    return iDatei, gesamtZeilen

import logging


def logAuswerten(db, logfile):
    """Logdatei auswerten und in die DB eintragen

    Args:
        db (MySQL-Connection): DB-Verbindung
        logfile (string): Pfad zur Logdatei

    Returns:
        None
    """
    logging.debug(f"logAuswerten: Auswertung der Logdatei {logfile}")
    # Hier kommt die Logauswertung und das Eintragen in die DB hin
    with open(logfile, "r") as f:
        for line in f:
            print(line.strip())
    return

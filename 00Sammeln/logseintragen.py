from dbparam import *
import os, mysql.connector
import logging


def logsEintragen(db, pfad):
    """Pfad in die Tabelle eintragen

    Args:
        db (MySQL-Connection): DB-Verbindung
        pfad (string): Pfad mit / am Ende

    Returns:
        string: Meldung
    """
    logging.debug(f"logsEintragen: Eintragen des Pfades {pfad} in DB-Tabelle {DBTBB}")
    if not os.path.exists(pfad):
        logging.fatal(f"logsEintragen: Pfad {pfad} existiert nicht.")
        return f"Pfad {pfad} existiert nicht."
    for root, dirs, files in os.walk(pfad):
        logging.debug("logsEintragen:root %s", root)
        logging.debug("logsEintragen:dirs= %s", dirs)
        logging.debug("logsEintragen:files %s", files)
        return
        break  # nur oberste Ebene

    with db.cursor() as cursor:
        # sql = f"INSERT INTO {DBTBB} (programm,parameter) VALUES ('{titel}','{pfad}')"
        # logging.debug(sql)
        # cursor.execute(sql)
        pass
    # db.commit()
    return "Pfad eingetragen"

from dbparam import DBTLOGS
import os, mysql.connector
import logging
from logauswerten import logAuswerten
from loganalyse import logAnalyse
from fhemnamen import nameReduzieren


def logsEintragen(db, pfad):
    if not os.path.exists(pfad):
        logging.fatal(f"logsEintragen: Pfad {pfad} existiert nicht.")
        return f"Pfad {pfad} existiert nicht."
    for root, dirs, files in os.walk(pfad):
        # logging.debug("logsEintragen:root %s", root)
        # logging.debug("logsEintragen:dirs= %s", dirs)
        # logging.debug("logsEintragen:files %s", files)
        for file in files:
            fileMitPfad = os.path.join(root, file)
            # Datei bekannt?
            basisName = nameReduzieren(file)
            return
            logfile = {"name": basisName, "path": fileMitPfad}
            with db.cursor() as cursor:
                sql = f"select typ from {DBTLOGS} where name='{file}'"
                cursor.execute(sql)
                result = cursor.fetchone()
                if result is None:
                    logging.debug(
                        f"logsEintragen: Datei {file} unbekannt, Eintrag erstellen"
                    )
                    typ = logAnalyse(fileMitPfad)
                    return

            logAuswerten(db, logfile)

            return

    with db.cursor() as cursor:
        # sql = f"INSERT INTO {DBTBB} (programm,parameter) VALUES ('{titel}','{pfad}')"
        # logging.debug(sql)
        # cursor.execute(sql)
        pass
    # db.commit()
    return
